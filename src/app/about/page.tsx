import type { Metadata } from "next";
import { AboutPageView } from "@/components/about/about-page-view";
import { getAboutPageContent, getCategories, getResources } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  const content = await getAboutPageContent();

  return {
    title: content.heroTitle || t("about.title"),
    description: content.heroDescription || t("about.description"),
  };
}

export default async function AboutPage() {
  const [content, resources, categories] = await Promise.all([
    getAboutPageContent(),
    getResources(),
    getCategories(),
  ]);

  const stateCount = new Set(resources.map((r) => r.state).filter(Boolean)).size;
  const resourceCount =
    resources.length >= 100 ? `${resources.length}+` : String(resources.length);

  return (
    <AboutPageView
      content={content}
      stats={{
        resourceCount,
        stateCount: String(stateCount),
        categoryCount: String(categories.length),
        freeLabel: "100%",
      }}
    />
  );
}
