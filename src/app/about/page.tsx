import type { Metadata } from "next";
import { getCmsPageBySlug } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("about.title"),
    description: t("about.description"),
  };
}

export default async function AboutPage() {
  const { t } = await getServerTranslator();
  const page = await getCmsPageBySlug("about");

  if (!page) {
    return (
      <div className="px-4 py-10 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="mb-6 text-3xl font-bold sm:text-4xl">{t("about.defaultTitle")}</h1>
          <div className="prose prose-lg max-w-none whitespace-pre-wrap text-base text-muted-foreground">
            {t("about.defaultContent")}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-6 text-3xl font-bold sm:text-4xl">{page.title}</h1>
        <div className="prose prose-lg max-w-none whitespace-pre-wrap text-base text-muted-foreground">
          {page.content}
        </div>
      </div>
    </div>
  );
}
