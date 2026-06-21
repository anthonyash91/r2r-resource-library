import type { Resource } from "@/types";
import { formatPhone, formatWebsiteDisplay, formatDate } from "@/lib/utils";
import {
  isRegionalResource,
  isStatewideResource,
  shouldShowCountiesServed,
} from "@/lib/resource-coverage";
import type { Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";
import { formatOperatingHours } from "@/i18n/localize-content";
import { getCategoryLabel } from "@/i18n/category-label";
import { PDF_RESOURCE_PAGE, PDF_THEME } from "@/lib/pdf/pdf-theme";
import {
  fitTextToHeight,
  fitTextToMaxChars,
  measureFixedPdfCard,
  type PdfLabeledValue,
  writeFixedPdfCard,
} from "@/lib/pdf/pdf-card";
import type { SavedResourcesPdfLabels } from "@/lib/pdf/saved-resources-pdf";

type PDFDocumentInstance = InstanceType<typeof import("pdfkit")>;

function buildFullAddress(resource: Resource): string | null {
  const parts: string[] = [];
  if (resource.address?.trim()) parts.push(resource.address.trim());
  const cityState = [resource.city, resource.state].filter(Boolean).join(", ");
  if (cityState) parts.push(cityState);
  if (resource.county?.trim()) parts.push(resource.county.trim());
  return parts.length > 0 ? parts.join("\n") : null;
}

function buildCountiesText(resource: Resource, labels: SavedResourcesPdfLabels): string | null {
  if (!shouldShowCountiesServed(resource)) return null;
  if (isStatewideResource(resource)) return labels.coverageStatewide;
  if (resource.served_counties?.length) return resource.served_counties.join(", ");
  return null;
}

function coverageNote(resource: Resource, labels: SavedResourcesPdfLabels): string | null {
  if (isStatewideResource(resource)) return labels.coverageStatewide;
  if (isRegionalResource(resource)) return labels.coverageRegional;
  return null;
}

function writeCategoryBadges(
  doc: PDFDocumentInstance,
  options: {
    x: number;
    y: number;
    width: number;
    categoryName: string | null;
    coverage: string | null;
  }
): number {
  const { fontSize, spacing } = PDF_RESOURCE_PAGE;
  const { x, width, categoryName, coverage } = options;
  const { pillHeight, pillPaddingX } = spacing;
  let y = options.y;

  if (!categoryName && !coverage) return y;

  let cursorX = x;

  if (categoryName) {
    doc.font("Helvetica-Bold").fontSize(fontSize.pill);
    const pillWidth = Math.min(width, doc.widthOfString(categoryName) + pillPaddingX * 2);
    const textY = y + (pillHeight - fontSize.pill) / 2 + 1;
    doc.save();
    doc
      .roundedRect(cursorX, y, pillWidth, pillHeight, 6)
      .fillColor(PDF_THEME.colors.badgeBg)
      .fill()
      .strokeColor(PDF_THEME.colors.badgeBorder)
      .lineWidth(0.5)
      .stroke();
    doc.restore();
    doc
      .font("Helvetica-Bold")
      .fontSize(fontSize.pill)
      .fillColor(PDF_THEME.colors.badgeFg)
      .text(categoryName, cursorX + pillPaddingX, textY, { width: pillWidth - pillPaddingX * 2, lineBreak: false });
    cursorX += pillWidth + 8;
  }

  if (coverage) {
    doc.font("Helvetica-Bold").fontSize(fontSize.pill);
    const pillWidth = Math.min(width - (cursorX - x), doc.widthOfString(coverage) + pillPaddingX * 2);
    const textY = y + (pillHeight - fontSize.pill) / 2 + 1;
    doc.save();
    doc
      .roundedRect(cursorX, y, pillWidth, pillHeight, 6)
      .fillColor(PDF_THEME.colors.badgeBg)
      .fill()
      .strokeColor(PDF_THEME.colors.badgeBorder)
      .lineWidth(0.5)
      .stroke();
    doc.restore();
    doc
      .font("Helvetica-Bold")
      .fontSize(fontSize.pill)
      .fillColor(PDF_THEME.colors.badgeFg)
      .text(coverage, cursorX + pillPaddingX, textY, { width: pillWidth - pillPaddingX * 2, lineBreak: false });
  }

  return y + pillHeight + spacing.cardGap;
}

function measureTitleCardHeight(
  doc: PDFDocumentInstance,
  x: number,
  width: number,
  resource: Resource,
  description: string,
  coverageLabel: string | null
): number {
  const { fontSize, spacing } = PDF_RESOURCE_PAGE;
  const innerW = width - spacing.cardPadding * 2;
  let body = description.trim();
  if (coverageLabel) body = `${coverageLabel}\n\n${body}`;

  doc.font("Helvetica-Bold").fontSize(fontSize.resourceName);
  const titleH = doc.heightOfString(resource.name, { width: innerW });
  doc.font("Helvetica").fontSize(fontSize.body);
  const bodyH = doc.heightOfString(body, { width: innerW, lineGap: spacing.lineGap });

  return spacing.cardPadding * 2 + titleH + spacing.titleBodyGap + bodyH;
}

function writeTitleCard(
  doc: PDFDocumentInstance,
  x: number,
  y: number,
  width: number,
  resource: Resource,
  description: string,
  coverageLabel: string | null
): number {
  const { fontSize, spacing } = PDF_RESOURCE_PAGE;
  const innerX = x + spacing.cardPadding;
  const innerW = width - spacing.cardPadding * 2;
  let body = description.trim();
  if (coverageLabel) body = `${coverageLabel}\n\n${body}`;

  const cardHeight = measureTitleCardHeight(doc, x, width, resource, description, coverageLabel);

  doc.save();
  doc
    .roundedRect(x, y, width, cardHeight, spacing.cardRadius)
    .fillColor(PDF_THEME.colors.card)
    .fill()
    .strokeColor(PDF_THEME.colors.border)
    .lineWidth(0.75)
    .stroke();
  doc.restore();

  doc
    .font("Helvetica-Bold")
    .fontSize(fontSize.resourceName)
    .fillColor(PDF_THEME.colors.foreground)
    .text(resource.name, innerX, y + spacing.cardPadding, { width: innerW });

  doc
    .font("Helvetica")
    .fontSize(fontSize.body)
    .fillColor(PDF_THEME.colors.muted)
    .text(body, innerX, doc.y + spacing.titleBodyGap, { width: innerW, lineGap: spacing.lineGap });

  return y + cardHeight + spacing.cardGap;
}

function buildContactEntries(
  resource: Resource,
  labels: SavedResourcesPdfLabels,
  locale: Locale
): PdfLabeledValue[] {
  const entries: PdfLabeledValue[] = [];
  const address = buildFullAddress(resource);
  if (address) entries.push({ label: "", value: address });
  if (resource.phone) {
    entries.push({ label: labels.phone, value: formatPhone(resource.phone), link: true });
  }
  if (resource.website) {
    entries.push({
      label: labels.website,
      value: formatWebsiteDisplay(resource.website) || resource.website,
      link: true,
    });
  }
  if (resource.email) {
    entries.push({ label: labels.email, value: resource.email, link: true });
  }
  if (resource.hours) {
    entries.push({
      label: labels.hours,
      value: formatOperatingHours(resource.hours, locale),
    });
  }
  return entries;
}

function measureLeftColumnHeight(
  doc: PDFDocumentInstance,
  options: {
    leftX: number;
    leftWidth: number;
    resource: Resource;
    description: string;
    coverageLabel: string | null;
    labels: SavedResourcesPdfLabels;
    services: string[];
    eligibility: string | null;
    notes: string | null;
  }
): number {
  const { leftWidth, resource, description, coverageLabel, labels, services, eligibility, notes } =
    options;
  const compact = PDF_RESOURCE_PAGE;
  let height = 0;

  height += measureTitleCardHeight(doc, options.leftX, leftWidth, resource, description, coverageLabel);

  if (services.length > 0) {
    height += measureFixedPdfCard(
      doc,
      leftWidth,
      { title: labels.services, listItems: services },
      compact
    );
  }
  if (eligibility) {
    height += measureFixedPdfCard(doc, leftWidth, { title: labels.eligibility, body: eligibility }, compact);
  }
  if (notes) {
    height += measureFixedPdfCard(doc, leftWidth, { title: labels.goodToKnow, body: notes }, compact);
  }

  return height;
}

function prepareContentForPage(
  doc: PDFDocumentInstance,
  resource: Resource,
  options: {
    leftX: number;
    leftWidth: number;
    coverageLabel: string | null;
    labels: SavedResourcesPdfLabels;
    services: string[];
    eligibility: string | null;
    notes: string | null;
    columnStartY: number;
    contentBottom: number;
  }
): { description: string; eligibility: string | null; notes: string | null } {
  const { fontSize, spacing, maxDescriptionChars, maxEligibilityChars, maxNotesChars } =
    PDF_RESOURCE_PAGE;
  const innerW = options.leftWidth - spacing.cardPadding * 2;
  const available = options.contentBottom - options.columnStartY - 8;

  let description = fitTextToMaxChars(resource.description, maxDescriptionChars);
  let eligibility = options.eligibility ? fitTextToMaxChars(options.eligibility, maxEligibilityChars) : null;
  let notes = options.notes ? fitTextToMaxChars(options.notes, maxNotesChars) : null;

  for (let attempt = 0; attempt < 8; attempt += 1) {
    const leftHeight = measureLeftColumnHeight(doc, {
      leftX: options.leftX,
      leftWidth: options.leftWidth,
      resource,
      description,
      coverageLabel: options.coverageLabel,
      labels: options.labels,
      services: options.services,
      eligibility,
      notes,
    });

    if (leftHeight <= available) {
      return { description, eligibility, notes };
    }

    const titleOnlyHeight = measureTitleCardHeight(
      doc,
      options.leftX,
      options.leftWidth,
      resource,
      "",
      options.coverageLabel
    );
    const otherHeight =
      leftHeight -
      measureTitleCardHeight(
        doc,
        options.leftX,
        options.leftWidth,
        resource,
        description,
        options.coverageLabel
      );
    const descBudget = Math.max(36, available - titleOnlyHeight - otherHeight - spacing.cardGap);

    description = fitTextToHeight(
      doc,
      resource.description,
      innerW,
      Math.max(24, descBudget - (options.coverageLabel ? 20 : 0)),
      fontSize.body,
      spacing.lineGap
    );

    if (attempt >= 4) {
      eligibility = eligibility
        ? fitTextToMaxChars(eligibility, Math.max(80, maxEligibilityChars - attempt * 40))
        : null;
      notes = notes ? fitTextToMaxChars(notes, Math.max(60, maxNotesChars - attempt * 30)) : null;
    }
  }

  return { description, eligibility, notes };
}

/** Renders one resource on the current page. Caller must addPage() before invoking. */
export function writeResourceSinglePage(
  doc: PDFDocumentInstance,
  options: {
    resource: Resource;
    labels: SavedResourcesPdfLabels;
    locale: Locale;
    marginLeft: number;
    contentWidth: number;
    contentTop: number;
    contentBottom: number;
  }
): void {
  const { resource, labels, locale, marginLeft, contentWidth, contentTop, contentBottom } = options;
  const { t } = createTranslator(locale);
  const compact = PDF_RESOURCE_PAGE;
  const { spacing } = compact;

  const leftWidth = Math.floor(contentWidth * 0.58);
  const rightWidth = contentWidth - leftWidth - spacing.columnGap;
  const leftX = marginLeft;
  const rightX = marginLeft + leftWidth + spacing.columnGap;

  const categoryName = resource.category ? getCategoryLabel(resource.category, t) : null;
  const coverage = coverageNote(resource, labels);
  const showCoverageLabel =
    isStatewideResource(resource) ||
    (isRegionalResource(resource) && shouldShowCountiesServed(resource));
  const titleCoverageLabel = showCoverageLabel ? coverage : null;

  let y = writeCategoryBadges(doc, {
    x: marginLeft,
    y: contentTop,
    width: contentWidth,
    categoryName,
    coverage,
  });

  const columnStartY = y;
  const services = resource.services.slice(0, PDF_RESOURCE_PAGE.maxServices);
  const eligibility = resource.eligibility?.trim() || null;
  const notes = resource.notes?.trim() || null;

  const { description, eligibility: fittedEligibility, notes: fittedNotes } =
    prepareContentForPage(doc, resource, {
      leftX,
      leftWidth,
      coverageLabel: titleCoverageLabel,
      labels,
      services,
      eligibility,
      notes,
      columnStartY,
      contentBottom,
    });

  let rightY = columnStartY;
  const contactEntries = buildContactEntries(resource, labels, locale);
  if (contactEntries.length > 0) {
    rightY = writeFixedPdfCard(doc, rightX, rightY, rightWidth, {
      title: labels.contactInfo,
      labeledValues: contactEntries,
    }, compact);
  }

  const counties = buildCountiesText(resource, labels);
  if (counties) {
    rightY = writeFixedPdfCard(doc, rightX, rightY, rightWidth, {
      title: labels.countiesServed,
      body: counties,
    }, compact);
  }

  const lastUpdatedText = t("resources.lastUpdated", {
    date: formatDate(resource.updated_at, locale),
  });
  if (rightY + 14 <= contentBottom) {
    doc
      .font("Helvetica")
      .fontSize(compact.fontSize.meta)
      .fillColor(PDF_THEME.colors.muted)
      .text(lastUpdatedText, rightX, rightY, { width: rightWidth, align: "center" });
  }

  let leftY = columnStartY;
  leftY = writeTitleCard(doc, leftX, leftY, leftWidth, resource, description, titleCoverageLabel);

  if (services.length > 0) {
    leftY = writeFixedPdfCard(doc, leftX, leftY, leftWidth, {
      title: labels.services,
      listItems: services,
    }, compact);
  }

  if (fittedEligibility) {
    leftY = writeFixedPdfCard(doc, leftX, leftY, leftWidth, {
      title: labels.eligibility,
      body: fittedEligibility,
      variant: "eligibility",
    }, compact);
  }

  if (fittedNotes) {
    writeFixedPdfCard(doc, leftX, leftY, leftWidth, {
      title: labels.goodToKnow,
      body: fittedNotes,
    }, compact);
  }
}
