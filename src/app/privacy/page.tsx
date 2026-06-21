import type { Metadata } from "next";
import { Shield } from "lucide-react";
import { LegalDocumentView } from "@/components/legal/legal-document-view";
import { getLegalDocumentContent } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const content = await getLegalDocumentContent("privacy");

  return {
    title: content.title,
    description: content.description,
  };
}

export default async function PrivacyPage() {
  const { t } = await getServerTranslator();
  const content = await getLegalDocumentContent("privacy");

  return (
    <LegalDocumentView
      icon={Shield}
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
