import type { Metadata } from "next";
import { AboutPageView } from "@/components/about/about-page-view";
import { getAboutPageContent, getCategories, getActiveResourceCount, getStates } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";
import { formatRoundedResourceStat } from "@/lib/utils";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  const content = await getAboutPageContent();

  return {
    title: content.heroTitle || t("about.title"),
    description: content.heroDescription || t("about.description"),
  };
}

export default async function AboutPage() {
  const { locale } = await getServerTranslator();
  const [content, activeResourceCount, categories, states] = await Promise.all([
    getAboutPageContent(),
    getActiveResourceCount(),
    getCategories(),
    getStates(),
  ]);

  const resourceCount = formatRoundedResourceStat(activeResourceCount, locale);
  const stateCount = states.length;

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
