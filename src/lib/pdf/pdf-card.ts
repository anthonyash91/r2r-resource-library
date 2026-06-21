import { PDF_RESOURCE_PAGE, PDF_THEME } from "@/lib/pdf/pdf-theme";

type PDFDocumentInstance = InstanceType<typeof import("pdfkit")>;

export interface PdfLabeledValue {
  label: string;
  value: string;
  link?: boolean;
}

export interface PdfFixedCardContent {
  title?: string;
  body?: string;
  lines?: string[];
  listItems?: string[];
  labeledValues?: PdfLabeledValue[];
}

function measureFixedCardHeight(
  doc: PDFDocumentInstance,
  width: number,
  content: PdfFixedCardContent,
  compact: typeof PDF_RESOURCE_PAGE
): number {
  const { fontSize, spacing } = compact;
  const innerW = width - spacing.cardPadding * 2;
  let height = spacing.cardPadding;

  if (content.title) {
    doc.font("Helvetica-Bold").fontSize(fontSize.sectionLabel);
    height += doc.heightOfString(content.title, { width: innerW }) + spacing.titleBodyGap;
  }

  if (content.body) {
    doc.font("Helvetica").fontSize(fontSize.body);
    height +=
      doc.heightOfString(content.body.trim(), { width: innerW, lineGap: spacing.lineGap }) +
      spacing.cardPadding;
    return height;
  }

  if (content.lines?.length) {
    doc.font("Helvetica").fontSize(fontSize.body);
    for (const line of content.lines) {
      height +=
        doc.heightOfString(line, { width: innerW, lineGap: spacing.lineGap }) + spacing.sectionGap;
    }
    height += spacing.cardPadding - spacing.sectionGap;
    return height;
  }

  if (content.labeledValues?.length) {
    doc.font("Helvetica").fontSize(fontSize.body);
    for (const entry of content.labeledValues) {
      const line = entry.label ? `${entry.label}: ${entry.value}` : entry.value;
      height +=
        doc.heightOfString(line, { width: innerW, lineGap: spacing.lineGap }) + spacing.sectionGap;
    }
    height += spacing.cardPadding - spacing.sectionGap;
    return height;
  }

  if (content.listItems?.length) {
    doc.font("Helvetica").fontSize(fontSize.body);
    for (const item of content.listItems) {
      height +=
        doc.heightOfString(item, { width: innerW, lineGap: spacing.lineGap }) + spacing.sectionGap;
    }
    height += spacing.cardPadding - spacing.sectionGap;
    return height;
  }

  return height + spacing.cardPadding;
}

function drawFixedCardBackground(
  doc: PDFDocumentInstance,
  x: number,
  y: number,
  width: number,
  height: number,
  compact: typeof PDF_RESOURCE_PAGE
): void {
  const { colors, spacing } = PDF_THEME;

  doc.save();
  doc
    .roundedRect(x, y, width, height, spacing.cardRadius)
    .fillColor(colors.card)
    .fill()
    .strokeColor(colors.border)
    .lineWidth(0.75)
    .stroke();
  doc.restore();
}

function writeFixedCardContent(
  doc: PDFDocumentInstance,
  x: number,
  y: number,
  width: number,
  content: PdfFixedCardContent,
  compact: typeof PDF_RESOURCE_PAGE
): void {
  const { fontSize, spacing } = compact;
  const innerX = x + spacing.cardPadding;
  const innerW = width - spacing.cardPadding * 2;
  let cursorY = y + spacing.cardPadding;

  if (content.title) {
    doc
      .font("Helvetica-Bold")
      .fontSize(fontSize.sectionLabel)
      .fillColor(PDF_THEME.colors.foreground)
      .text(content.title, innerX, cursorY, { width: innerW });
    cursorY = doc.y + spacing.titleBodyGap;
  }

  if (content.body) {
    doc
      .font("Helvetica")
      .fontSize(fontSize.body)
      .fillColor(PDF_THEME.colors.muted)
      .text(content.body.trim(), innerX, cursorY, { width: innerW, lineGap: spacing.lineGap });
    return;
  }

  if (content.lines?.length) {
    doc.font("Helvetica").fontSize(fontSize.body).fillColor(PDF_THEME.colors.muted);
    for (const line of content.lines) {
      doc.text(line, innerX, cursorY, { width: innerW, lineGap: spacing.lineGap });
      cursorY = doc.y + spacing.sectionGap;
    }
    return;
  }

  if (content.labeledValues?.length) {
    doc.font("Helvetica").fontSize(fontSize.body);
    for (const entry of content.labeledValues) {
      if (!entry.label) {
        doc
          .fillColor(PDF_THEME.colors.muted)
          .text(entry.value, innerX, cursorY, { width: innerW, lineGap: spacing.lineGap });
      } else {
        const prefix = `${entry.label}: `;
        doc
          .fillColor(PDF_THEME.colors.muted)
          .text(prefix, innerX, cursorY, { continued: true, lineBreak: false });
        doc
          .fillColor(entry.link ? PDF_THEME.colors.primary : PDF_THEME.colors.muted)
          .text(entry.value, { width: innerW, lineGap: spacing.lineGap });
      }
      cursorY = doc.y + spacing.sectionGap;
    }
    return;
  }

  if (content.listItems?.length) {
    doc.font("Helvetica").fontSize(fontSize.body).fillColor(PDF_THEME.colors.foreground);
    for (const item of content.listItems) {
      doc.text(item, innerX, cursorY, {
        width: innerW,
        lineGap: spacing.lineGap,
      });
      cursorY = doc.y + spacing.sectionGap;
    }
  }
}

/** Draw a card at a fixed Y on the current page. Never adds pages. Returns Y below the card. */
export function writeFixedPdfCard(
  doc: PDFDocumentInstance,
  x: number,
  y: number,
  width: number,
  content: PdfFixedCardContent,
  compact: typeof PDF_RESOURCE_PAGE = PDF_RESOURCE_PAGE
): number {
  const cardHeight = measureFixedCardHeight(doc, width, content, compact);
  drawFixedCardBackground(doc, x, y, width, cardHeight, compact);
  writeFixedCardContent(doc, x, y, width, content, compact);
  return y + cardHeight + compact.spacing.cardGap;
}

export function measureFixedPdfCard(
  doc: PDFDocumentInstance,
  width: number,
  content: PdfFixedCardContent,
  compact: typeof PDF_RESOURCE_PAGE = PDF_RESOURCE_PAGE
): number {
  return measureFixedCardHeight(doc, width, content, compact);
}

export function fitTextToHeight(
  doc: PDFDocumentInstance,
  text: string,
  width: number,
  maxHeight: number,
  fontSize: number,
  lineGap: number
): string {
  const trimmed = text.trim();
  if (!trimmed) return "";

  doc.font("Helvetica").fontSize(fontSize);
  if (doc.heightOfString(trimmed, { width, lineGap }) <= maxHeight) {
    return trimmed;
  }

  let lo = 0;
  let hi = trimmed.length;

  while (lo < hi) {
    const mid = Math.ceil((lo + hi) / 2);
    const candidate = `${trimmed.slice(0, mid).trimEnd()}…`;
    if (doc.heightOfString(candidate, { width, lineGap }) <= maxHeight) {
      lo = mid;
    } else {
      hi = mid - 1;
    }
  }

  if (lo >= trimmed.length) return trimmed;
  return `${trimmed.slice(0, lo).trimEnd()}…`;
}

export function fitTextToMaxChars(text: string, maxChars: number): string {
  const trimmed = text.trim();
  if (trimmed.length <= maxChars) return trimmed;
  return `${trimmed.slice(0, maxChars - 1).trimEnd()}…`;
}
