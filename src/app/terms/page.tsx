import type { Metadata } from "next";
import { FileText } from "lucide-react";
import { LegalDocumentView } from "@/components/legal/legal-document-view";
import { getLegalDocumentContent } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const content = await getLegalDocumentContent("terms");

  return {
    title: content.title,
    description: content.description,
  };
}

export default async function TermsPage() {
  const { t } = await getServerTranslator();
  const content = await getLegalDocumentContent("terms");

  return (
    <LegalDocumentView
      icon={FileText}
      title={content.title}
      description={content.description}
      intro={content.intro}
      sections={content.sections}
      lastUpdated={t("legal.lastUpdated", { date: content.lastUpdatedDate })}
      contactLinkLabel={t("legal.contactLink")}
      contactPrompt={content.contactPrompt}
    />
  );
}
