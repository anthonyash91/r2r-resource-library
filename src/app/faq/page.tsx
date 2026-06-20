import type { Metadata } from "next";
import { getFaqs } from "@/lib/data";
import { FaqAccordion } from "./faq-accordion";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("faq.title"),
    description: t("faq.description"),
  };
}

function categoryLabel(t: (key: string) => string, category: string) {
  const normalized = category.toLowerCase().replace(/\s+/g, "");
  if (normalized === "general") return t("faq.general");
  if (normalized === "usingthesite") return t("faq.usingTheSite");
  return category;
}

export default async function FaqPage() {
  const { t } = await getServerTranslator();
  const faqs = await getFaqs();

  const grouped = faqs.reduce(
    (acc, faq) => {
      const cat = faq.category ?? t("faq.general");
      if (!acc[cat]) acc[cat] = [];
      acc[cat].push(faq);
      return acc;
    },
    {} as Record<string, typeof faqs>
  );

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <header className="mb-10">
          <h1 className="mb-2 text-3xl font-bold sm:text-4xl">{t("faq.heading")}</h1>
          <p className="text-lg text-muted-foreground">{t("faq.intro")}</p>
        </header>

        {Object.entries(grouped).map(([category, categoryFaqs]) => (
          <section key={category} className="mb-10" aria-labelledby={`faq-${category}`}>
            <h2 id={`faq-${category}`} className="mb-4 text-xl font-bold">
              {categoryLabel(t, category)}
            </h2>
            <FaqAccordion faqs={categoryFaqs} />
          </section>
        ))}
      </div>
    </div>
  );
}
