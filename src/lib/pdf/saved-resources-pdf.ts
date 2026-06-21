import { createRequire } from "node:module";
import type { Resource } from "@/types";
import { formatDate } from "@/lib/utils";
import type { Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";
import {
  type SavedResourcesPdfBranding,
  beginSubsequentPdfPage,
  getPdfContentBottom,
  paintPdfPageBackground,
  PDF_PAGE_HEADER_HEIGHT,
  writePdfCoverBranding,
  writePdfIntroCard,
} from "@/lib/pdf/pdf-branding";
import { writeResourceSinglePage } from "@/lib/pdf/pdf-resource-detail-layout";

const require = createRequire(import.meta.url);

function createPdfDocument(options: { margin: number; size: string }) {
  const PDFDocument = require("pdfkit") as typeof import("pdfkit");
  return new PDFDocument(options);
}

export interface SavedResourcesPdfLabels {
  documentTitle: string;
  preparedFor: string;
  generatedOn: string;
  resourceCount: string;
  category: string;
  description: string;
  location: string;
  address: string;
  phone: string;
  email: string;
  website: string;
  hours: string;
  eligibility: string;
  goodToKnow: string;
  services: string;
  countiesServed: string;
  contactInfo: string;
  coverageStatewide: string;
  coverageRegional: string;
  footer: string;
}

export function getSavedResourcesPdfLabels(locale: Locale): SavedResourcesPdfLabels {
  const { t } = createTranslator(locale);

  return {
    documentTitle: t("saved.pdf.documentTitle"),
    preparedFor: t("saved.pdf.preparedFor"),
    generatedOn: t("saved.pdf.generatedOn"),
    resourceCount: t("saved.pdf.resourceCount"),
    category: t("resources.category"),
    description: t("saved.pdf.description"),
    location: t("saved.pdf.location"),
    address: t("saved.pdf.address"),
    phone: t("resources.phone"),
    email: t("resources.email"),
    website: t("resources.website"),
    hours: t("resources.hours"),
    eligibility: t("resources.eligibilityRequirements"),
    goodToKnow: t("resources.additionalInfo"),
    services: t("resources.servicesOffered"),
    countiesServed: t("resources.countiesServed"),
    contactInfo: t("resources.contactInfo"),
    coverageStatewide: t("resources.coverageStatewide"),
    coverageRegional: t("resources.coverageRegional"),
    footer: t("saved.pdf.footer"),
  };
}

export async function generateSavedResourcesPdf(options: {
  resources: Resource[];
  labels: SavedResourcesPdfLabels;
  locale: Locale;
  recipientName?: string | null;
  branding: SavedResourcesPdfBranding;
}): Promise<Buffer> {
  const { resources, labels, locale, recipientName, branding } = options;

  return new Promise((resolve, reject) => {
    const doc = createPdfDocument({ margin: 54, size: "LETTER" });
    const chunks: Buffer[] = [];

    doc.on("data", (chunk: Buffer) => chunks.push(chunk));
    doc.on("end", () => resolve(Buffer.concat(chunks)));
    doc.on("error", reject);

    const marginLeft = doc.page.margins.left;
    const contentWidth = doc.page.width - doc.page.margins.left - doc.page.margins.right;
    const pageWidth = doc.page.width;
    let pageNumber = 1;

    const layoutOptions = { marginLeft, contentWidth, pageWidth };

    doc.on("pageAdded", () => {
      pageNumber += 1;
      beginSubsequentPdfPage(doc, branding.brandName, labels.footer, layoutOptions);
    });

    paintPdfPageBackground(doc);

    const contentTop = doc.page.margins.top + PDF_PAGE_HEADER_HEIGHT;

    writePdfCoverBranding(doc, branding, layoutOptions);

    const introLines = [
      labels.generatedOn.replace("{date}", formatDate(new Date().toISOString(), locale)),
      labels.resourceCount.replace("{count}", String(resources.length)),
    ];
    if (recipientName?.trim()) {
      introLines.unshift(labels.preparedFor.replace("{name}", recipientName.trim()));
    }

    writePdfIntroCard(doc, {
      marginLeft,
      contentWidth,
      title: labels.documentTitle,
      lines: introLines,
    });

    const contentBottom = () =>
      getPdfContentBottom(doc, {
        isFirstPage: false,
        footerText: labels.footer,
        contentWidth,
      });

    resources.forEach((resource) => {
      doc.addPage();
      writeResourceSinglePage(doc, {
        resource,
        labels,
        locale,
        marginLeft,
        contentWidth,
        contentTop,
        contentBottom: contentBottom(),
      });
    });

    doc.end();
  });
}
