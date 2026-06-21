import type { Metadata } from "next";
import { FaqPageView } from "@/components/faq/faq-page-view";
import { getFaqs } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("faq.title"),
    description: t("faq.description"),
  };
}

export default async function FaqPage() {
  const faqs = await getFaqs();

  return <FaqPageView faqs={faqs} />;
}
