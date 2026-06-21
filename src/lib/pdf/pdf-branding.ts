import fs from "node:fs";
import path from "node:path";
import type { SiteBranding } from "@/i18n/localize-content";
import type { Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";
import { PDF_THEME } from "@/lib/pdf/pdf-theme";

export const PDF_PAGE_HEADER_HEIGHT = 26;
export const PDF_PAGE_FOOTER_HEIGHT = 32;

export interface SavedResourcesPdfBranding {
  brandName: string;
  brandTagline: string;
  brandDescription: string;
  logo?: string | Buffer | null;
  coverLogo?: string | Buffer | null;
}

function extractEmbeddedPngFromSvg(svgPath: string): Buffer | null {
  if (!fs.existsSync(svgPath)) return null;

  const svg = fs.readFileSync(svgPath, "utf8");
  const match = svg.match(/href="data:image\/png;base64,([^"]+)"/);
  if (!match?.[1]) return null;

  return Buffer.from(match[1], "base64");
}

function resolveLogoFromSvg(relativePath: string): Buffer | null {
  return extractEmbeddedPngFromSvg(path.join(process.cwd(), "public", relativePath));
}

export function resolvePdfLogoImages(): {
  logo: string | Buffer | null;
  coverLogo: string | Buffer | null;
} {
  const logoPngPath = path.join(process.cwd(), "public", "logo.png");
  const greenLogo = resolveLogoFromSvg("green-logo.svg");
  const whiteLogo = resolveLogoFromSvg("white-logo.svg");

  return {
    logo: fs.existsSync(logoPngPath) ? logoPngPath : greenLogo,
    coverLogo: whiteLogo ?? greenLogo ?? (fs.existsSync(logoPngPath) ? logoPngPath : null),
  };
}

export function getSavedResourcesPdfBranding(
  locale: Locale,
  siteBranding: SiteBranding
): SavedResourcesPdfBranding {
  const { t } = createTranslator(locale);
  const logos = resolvePdfLogoImages();

  return {
    brandName: siteBranding.brandName,
    brandTagline: t("saved.pdf.brandTagline"),
    brandDescription: t("saved.pdf.brandDescription"),
    logo: logos.logo,
    coverLogo: logos.coverLogo,
  };
}

type PDFDocumentInstance = InstanceType<typeof import("pdfkit")>;

export function paintPdfPageBackground(doc: PDFDocumentInstance): void {
  doc.save();
  doc.rect(0, 0, doc.page.width, doc.page.height).fill(PDF_THEME.colors.background);
  doc.restore();
}

export function writePdfCoverBranding(
  doc: PDFDocumentInstance,
  branding: SavedResourcesPdfBranding,
  options: { contentWidth: number; marginLeft: number; pageWidth: number }
): number {
  const { contentWidth, marginLeft, pageWidth } = options;
  const { colors, fontSize, spacing } = PDF_THEME;
  const bandHeight = 108;
  const logoSize = 52;
  const textX = marginLeft + (branding.coverLogo ? logoSize + 14 : 0);
  const textWidth = contentWidth - (branding.coverLogo ? logoSize + 14 : 0);

  doc.save();
  doc.rect(0, 0, pageWidth, bandHeight).fill(colors.primaryDark);
  doc.restore();

  const bandTextY = 28;

  if (branding.coverLogo) {
    doc.image(branding.coverLogo, marginLeft, bandTextY - 4, { fit: [logoSize, logoSize] });
  }

  doc
    .font("Helvetica-Bold")
    .fontSize(fontSize.coverBrand)
    .fillColor(colors.white)
    .text(branding.brandName, textX, bandTextY, { width: textWidth });

  doc
    .font("Helvetica-Bold")
    .fontSize(fontSize.coverTagline)
    .fillColor(colors.primaryLight)
    .text(branding.brandTagline, textX, doc.y + 6, { width: textWidth });

  const contentStartY = bandHeight + 20;

  doc
    .font("Helvetica")
    .fontSize(fontSize.coverDescription)
    .fillColor(colors.muted)
    .text(branding.brandDescription, marginLeft, contentStartY, {
      width: contentWidth,
      lineGap: spacing.lineGap,
    });

  doc.y = doc.y + 16;

  doc
    .moveTo(marginLeft, doc.y)
    .lineTo(marginLeft + contentWidth, doc.y)
    .strokeColor(colors.primary)
    .lineWidth(2)
    .stroke();

  doc.y += 18;
  return doc.y;
}

export function writePdfIntroCard(
  doc: PDFDocumentInstance,
  options: {
    marginLeft: number;
    contentWidth: number;
    title: string;
    lines: string[];
  }
): void {
  const { marginLeft, contentWidth, title, lines } = options;
  const { colors, fontSize, spacing } = PDF_THEME;
  const cardTop = doc.y;
  const innerX = marginLeft + spacing.cardPadding;
  const innerW = contentWidth - spacing.cardPadding * 2;

  doc.font("Helvetica-Bold").fontSize(fontSize.coverTitle);
  const titleHeight = doc.heightOfString(title, { width: innerW });
  doc.font("Helvetica").fontSize(fontSize.coverMeta);
  const linesHeight = lines.reduce(
    (total, line) => total + doc.heightOfString(line, { width: innerW, lineGap: spacing.lineGap }) + 4,
    0
  );
  const cardHeight = spacing.cardPadding * 2 + titleHeight + linesHeight + 12;

  doc.save();
  doc
    .roundedRect(marginLeft, cardTop, contentWidth, cardHeight, spacing.cardRadius)
    .fillColor(colors.card)
    .fill()
    .strokeColor(colors.border)
    .lineWidth(1)
    .stroke();
  doc
    .roundedRect(marginLeft, cardTop, spacing.accentBarWidth, cardHeight, spacing.cardRadius)
    .fillColor(colors.primary)
    .fill();
  doc.restore();

  doc.y = cardTop + spacing.cardPadding;
  doc.x = innerX;

  doc
    .font("Helvetica-Bold")
    .fontSize(fontSize.coverTitle)
    .fillColor(colors.foreground)
    .text(title, { width: innerW });

  doc.moveDown(0.4);
  doc.font("Helvetica").fontSize(fontSize.coverMeta).fillColor(colors.muted);

  lines.forEach((line) => {
    doc.text(line, { width: innerW, lineGap: spacing.lineGap });
    doc.moveDown(0.15);
  });

  doc.x = marginLeft;
  doc.y = cardTop + cardHeight + spacing.cardGap;
}

export function writePdfPageHeader(
  doc: PDFDocumentInstance,
  brandName: string,
  options: { marginLeft: number; contentWidth: number }
): void {
  const { marginLeft, contentWidth } = options;
  const { colors, fontSize } = PDF_THEME;
  const headerY = doc.page.margins.top - 14;

  doc
    .font("Helvetica-Bold")
    .fontSize(fontSize.pageHeader)
    .fillColor(colors.primaryDark)
    .text(brandName, marginLeft, headerY, { width: contentWidth, align: "center", lineBreak: false });
}

export function writePdfPageFooter(
  doc: PDFDocumentInstance,
  footerText: string,
  options: { marginLeft: number; contentWidth: number }
): void {
  const { marginLeft, contentWidth } = options;
  const { colors, fontSize } = PDF_THEME;

  doc.font("Helvetica").fontSize(fontSize.footer);
  const textHeight = doc.heightOfString(footerText, {
    width: contentWidth,
    align: "center",
    lineGap: 2,
  });
  const footerY = doc.page.height - doc.page.margins.bottom - textHeight;

  doc
    .fillColor(colors.muted)
    .text(footerText, marginLeft, footerY, {
      width: contentWidth,
      align: "center",
      lineGap: 2,
    });
}

export function beginSubsequentPdfPage(
  doc: PDFDocumentInstance,
  brandName: string,
  footerText: string,
  options: { marginLeft: number; contentWidth: number; pageWidth: number }
): void {
  paintPdfPageBackground(doc);
  writePdfPageHeader(doc, brandName, { marginLeft: options.marginLeft, contentWidth: options.contentWidth });
  writePdfPageFooter(doc, footerText, { marginLeft: options.marginLeft, contentWidth: options.contentWidth });
  doc.y = doc.page.margins.top + PDF_PAGE_HEADER_HEIGHT;
  doc.x = options.marginLeft;
}

export function getPdfContentBottom(
  doc: PDFDocumentInstance,
  options: { isFirstPage: boolean; footerText?: string; contentWidth?: number }
): number {
  const { fontSize } = PDF_THEME;
  let footerReserve = options.isFirstPage ? 0 : PDF_PAGE_FOOTER_HEIGHT;

  if (!options.isFirstPage && options.footerText && options.contentWidth) {
    doc.font("Helvetica").fontSize(fontSize.footer);
    const textHeight = doc.heightOfString(options.footerText, {
      width: options.contentWidth,
      align: "center",
      lineGap: 2,
    });
    footerReserve = Math.max(PDF_PAGE_FOOTER_HEIGHT, textHeight + 8);
  }

  return doc.page.height - doc.page.margins.bottom - footerReserve;
}
