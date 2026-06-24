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
  splitTextToHeight,
  type PdfLabeledValue,
  writeFixedPdfCard,
} from "@/lib/pdf/pdf-card";
import type { SavedResourcesPdfLabels } from "@/lib/pdf/saved-resources-pdf";

type PDFDocumentInstance = InstanceType<typeof import("pdfkit")>;

interface ResourcePdfLayoutContext {
  doc: PDFDocumentInstance;
  contentTop: number;
  getContentBottom: () => number;
  newPage: () => void;
  y: number;
}

function advancePage(ctx: ResourcePdfLayoutContext): void {
  ctx.newPage();
  ctx.y = ctx.contentTop;
}

function ensureSpace(ctx: ResourcePdfLayoutContext, neededHeight: number): void {
  if (ctx.y + neededHeight > ctx.getContentBottom()) {
    advancePage(ctx);
  }
}

function drawCardBackground(
  doc: PDFDocumentInstance,
  x: number,
  y: number,
  width: number,
  height: number,
  variant: "default" | "eligibility" = "default"
): void {
  const { colors } = PDF_THEME;
  const { cardRadius } = PDF_RESOURCE_PAGE.spacing;
  const isEligibility = variant === "eligibility";

  doc.save();
  doc
    .roundedRect(x, y, width, height, cardRadius)
    .fillColor(isEligibility ? colors.eligibilityBg : colors.card)
    .fill()
    .strokeColor(isEligibility ? colors.eligibilityBorder : colors.border)
    .lineWidth(0.75)
    .stroke();
  doc.restore();
}

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

function writePaginatedBodyCard(
  ctx: ResourcePdfLayoutContext,
  x: number,
  width: number,
  options: {
    title: string;
    body: string;
    variant?: "default" | "eligibility";
  }
): void {
  const { doc } = ctx;
  const { fontSize, spacing } = PDF_RESOURCE_PAGE;
  const innerX = x + spacing.cardPadding;
  const innerW = width - spacing.cardPadding * 2;
  let remaining = options.body.trim();
  let segment = 0;

  while (segment === 0 || remaining) {
    ensureSpace(ctx, spacing.cardPadding * 2 + fontSize.sectionLabel + 20);

    doc.font("Helvetica-Bold").fontSize(fontSize.sectionLabel);
    const titleText = segment === 0 ? options.title : `${options.title} (${segment + 1})`;
    const titleHeight = doc.heightOfString(titleText, { width: innerW });

    const textBudget =
      ctx.getContentBottom() - ctx.y - spacing.cardPadding * 2 - titleHeight - spacing.titleBodyGap;

    doc.font("Helvetica").fontSize(fontSize.body);
    const { head, tail } = splitTextToHeight(
      doc,
      remaining,
      innerW,
      Math.max(24, textBudget),
      fontSize.body,
      spacing.lineGap
    );

    if (!head && remaining) {
      advancePage(ctx);
      continue;
    }

    const bodyHeight = doc.heightOfString(head, { width: innerW, lineGap: spacing.lineGap });
    const cardHeight =
      spacing.cardPadding * 2 + titleHeight + spacing.titleBodyGap + bodyHeight;
    const cardY = ctx.y;

    drawCardBackground(doc, x, cardY, width, cardHeight, options.variant);

    doc
      .font("Helvetica-Bold")
      .fontSize(fontSize.sectionLabel)
      .fillColor(PDF_THEME.colors.foreground)
      .text(titleText, innerX, cardY + spacing.cardPadding, { width: innerW });

    doc
      .font("Helvetica")
      .fontSize(fontSize.body)
      .fillColor(PDF_THEME.colors.muted)
      .text(head, innerX, doc.y + spacing.titleBodyGap, { width: innerW, lineGap: spacing.lineGap });

    ctx.y = cardY + cardHeight + spacing.cardGap;
    remaining = tail;
    segment += 1;

    if (remaining) {
      advancePage(ctx);
    }
  }
}

function writePaginatedServicesCard(
  ctx: ResourcePdfLayoutContext,
  x: number,
  width: number,
  title: string,
  services: string[]
): void {
  const { doc } = ctx;
  const { fontSize, spacing } = PDF_RESOURCE_PAGE;
  const innerX = x + spacing.cardPadding;
  const innerW = width - spacing.cardPadding * 2;
  let index = 0;
  let segment = 0;

  while (index < services.length) {
    ensureSpace(ctx, spacing.cardPadding * 2 + fontSize.sectionLabel + 20);

    doc.font("Helvetica-Bold").fontSize(fontSize.sectionLabel);
    const titleText = segment === 0 ? title : `${title} (${segment + 1})`;
    const titleHeight = doc.heightOfString(titleText, { width: innerW });

    const cardY = ctx.y;
    let cursorY = cardY + spacing.cardPadding + titleHeight + spacing.titleBodyGap;
    const bottomLimit = ctx.getContentBottom() - spacing.cardPadding;
    const itemsInSegment: string[] = [];

    doc.font("Helvetica").fontSize(fontSize.body);
    while (index < services.length) {
      const item = services[index];
      const itemHeight =
        doc.heightOfString(item, { width: innerW, lineGap: spacing.lineGap }) + spacing.sectionGap;
      if (cursorY + itemHeight > bottomLimit && itemsInSegment.length > 0) {
        break;
      }
      itemsInSegment.push(item);
      cursorY += itemHeight;
      index += 1;
    }

    const cardHeight = cursorY + spacing.cardPadding - cardY;
    drawCardBackground(doc, x, cardY, width, cardHeight);

    doc
      .font("Helvetica-Bold")
      .fontSize(fontSize.sectionLabel)
      .fillColor(PDF_THEME.colors.foreground)
      .text(titleText, innerX, cardY + spacing.cardPadding, { width: innerW });

    let itemY = cardY + spacing.cardPadding + titleHeight + spacing.titleBodyGap;
    doc.font("Helvetica").fontSize(fontSize.body);
    for (const item of itemsInSegment) {
      doc
        .fillColor(PDF_THEME.colors.checkAccent)
        .text("✓ ", innerX, itemY, { continued: true, lineBreak: false });
      doc
        .fillColor(PDF_THEME.colors.foreground)
        .text(item, { width: innerW, lineGap: spacing.lineGap });
      itemY = doc.y + spacing.sectionGap;
    }

    ctx.y = cardY + cardHeight + spacing.cardGap;
    segment += 1;

    if (index < services.length) {
      advancePage(ctx);
    }
  }
}

function writeTitleAndDescription(
  ctx: ResourcePdfLayoutContext,
  x: number,
  width: number,
  resource: Resource,
  description: string,
  coverageLabel: string | null
): void {
  const { doc } = ctx;
  const { fontSize, spacing } = PDF_RESOURCE_PAGE;
  const innerX = x + spacing.cardPadding;
  const innerW = width - spacing.cardPadding * 2;
  let remaining = description.trim();
  let segment = 0;

  while (segment === 0 || remaining) {
    ensureSpace(ctx, spacing.cardPadding * 2 + fontSize.resourceName + 20);

    const segmentText =
      segment === 0 && coverageLabel ? `${coverageLabel}\n\n${remaining}` : remaining;

    doc.font(segment === 0 ? "Helvetica-Bold" : "Helvetica").fontSize(
      segment === 0 ? fontSize.resourceName : fontSize.meta
    );
    const nameHeight =
      doc.heightOfString(resource.name, { width: innerW }) + spacing.titleBodyGap;

    const textBudget =
      ctx.getContentBottom() - ctx.y - spacing.cardPadding * 2 - nameHeight - spacing.cardPadding;

    doc.font("Helvetica").fontSize(fontSize.body);
    const { head, tail } = splitTextToHeight(
      doc,
      segmentText,
      innerW,
      Math.max(24, textBudget),
      fontSize.body,
      spacing.lineGap
    );

    if (!head && remaining) {
      advancePage(ctx);
      continue;
    }

    const bodyHeight = doc.heightOfString(head, { width: innerW, lineGap: spacing.lineGap });
    const cardHeight = spacing.cardPadding * 2 + nameHeight + bodyHeight;
    const cardY = ctx.y;

    drawCardBackground(doc, x, cardY, width, cardHeight);

    doc
      .font(segment === 0 ? "Helvetica-Bold" : "Helvetica")
      .fontSize(segment === 0 ? fontSize.resourceName : fontSize.meta)
      .fillColor(segment === 0 ? PDF_THEME.colors.foreground : PDF_THEME.colors.muted)
      .text(resource.name, innerX, cardY + spacing.cardPadding, { width: innerW });

    doc
      .font("Helvetica")
      .fontSize(fontSize.body)
      .fillColor(PDF_THEME.colors.muted)
      .text(head, innerX, doc.y + spacing.titleBodyGap, { width: innerW, lineGap: spacing.lineGap });

    ctx.y = cardY + cardHeight + spacing.cardGap;
    remaining = tail;
    segment += 1;

    if (remaining) {
      advancePage(ctx);
    }
  }
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

/** Renders one resource across as many pages as needed. Caller must addPage() before invoking. */
export function writeResourceSinglePage(
  doc: PDFDocumentInstance,
  options: {
    resource: Resource;
    labels: SavedResourcesPdfLabels;
    locale: Locale;
    marginLeft: number;
    contentWidth: number;
    contentTop: number;
    getContentBottom: () => number;
    newPage: () => void;
  }
): void {
  const { resource, labels, locale, marginLeft, contentWidth, contentTop, getContentBottom, newPage } =
    options;
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
  const contentBottom = getContentBottom();

  const contactEntries = buildContactEntries(resource, labels, locale);
  let rightColumnY = columnStartY;

  if (contactEntries.length > 0) {
    rightColumnY = writeFixedPdfCard(
      doc,
      rightX,
      rightColumnY,
      rightWidth,
      { title: labels.contactInfo, labeledValues: contactEntries },
      compact
    );
  }

  const counties = buildCountiesText(resource, labels);
  if (counties) {
    rightColumnY = writeFixedPdfCard(
      doc,
      rightX,
      rightColumnY,
      rightWidth,
      { title: labels.countiesServed, body: counties },
      compact
    );
  }

  const lastUpdatedText = t("resources.lastUpdated", {
    date: formatDate(resource.updated_at, locale),
  });
  if (rightColumnY + 14 <= contentBottom) {
    doc
      .font("Helvetica")
      .fontSize(compact.fontSize.meta)
      .fillColor(PDF_THEME.colors.muted)
      .text(lastUpdatedText, rightX, rightColumnY, {
        width: rightWidth,
        align: "center",
      });
  }

  const ctx: ResourcePdfLayoutContext = {
    doc,
    contentTop,
    getContentBottom,
    newPage,
    y: columnStartY,
  };

  writeTitleAndDescription(
    ctx,
    leftX,
    leftWidth,
    resource,
    resource.description,
    titleCoverageLabel
  );

  const services = resource.services.filter(Boolean);
  if (services.length > 0) {
    writePaginatedServicesCard(ctx, leftX, leftWidth, labels.services, services);
  }

  const eligibility = resource.eligibility?.trim();
  if (eligibility) {
    writePaginatedBodyCard(ctx, leftX, leftWidth, {
      title: labels.eligibility,
      body: eligibility,
      variant: "eligibility",
    });
  }

  const notes = resource.notes?.trim();
  if (notes) {
    writePaginatedBodyCard(ctx, leftX, leftWidth, {
      title: labels.goodToKnow,
      body: notes,
    });
  }
}
