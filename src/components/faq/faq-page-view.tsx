"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  BookOpen,
  HelpCircle,
  Mail,
  MessageCircle,
} from "lucide-react";
import { PageHeroBand } from "@/components/layout/page-hero-band";
import { Card } from "@/components/ui/card";
import { SearchField } from "@/components/ui/search-field";
import { FaqAccordion } from "@/components/faq/faq-accordion";
import { FAQ_CATEGORIES } from "@/lib/faq-categories";
import { cn, pageSectionPadding } from "@/lib/utils";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { useTranslations } from "@/i18n/locale-context";
import type { Faq } from "@/types";

interface FaqPageViewProps {
  faqs: Faq[];
}

type CategoryFilter = "all" | (typeof FAQ_CATEGORIES)[number]["value"];

function normalizeCategory(category: string | null | undefined, fallback: string): string {
  return category?.trim() || fallback;
}

export function FaqPageView({ faqs }: FaqPageViewProps) {
  const { t } = useTranslations();
  const [query, setQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState<CategoryFilter>("all");

  const generalFallback = t("faq.general");

  const categoryFilters = useMemo(
    () => [
      { value: "all" as const, label: t("faq.filterAll") },
      ...FAQ_CATEGORIES.map(({ value, labelKey }) => ({
        value,
        label: t(labelKey),
      })),
    ],
    [t]
  );

  const filteredFaqs = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    return faqs.filter((faq) => {
      const category = normalizeCategory(faq.category, generalFallback);
      const matchesCategory =
        activeCategory === "all" ||
        category.toLowerCase() === activeCategory.toLowerCase();

      if (!matchesCategory) return false;
      if (!normalizedQuery) return true;

      return (
        faq.question.toLowerCase().includes(normalizedQuery) ||
        faq.answer.toLowerCase().includes(normalizedQuery)
      );
    });
  }, [faqs, query, activeCategory, generalFallback]);

  const grouped = useMemo(() => {
    const groups = new Map<string, Faq[]>();

    for (const faq of filteredFaqs) {
      const category = normalizeCategory(faq.category, generalFallback);
      const existing = groups.get(category) ?? [];
      existing.push(faq);
      groups.set(category, existing);
    }

    const orderedCategories =
      activeCategory === "all"
        ? FAQ_CATEGORIES.map(({ value }) => value).filter((value) => groups.has(value))
        : groups.has(activeCategory)
          ? [activeCategory]
          : [];

    for (const category of groups.keys()) {
      if (!orderedCategories.includes(category as CategoryFilter)) {
        orderedCategories.push(category);
      }
    }

    return orderedCategories
      .map((category) => {
        const items = groups.get(category) ?? [];
        const labelKey = FAQ_CATEGORIES.find(
          (item) => item.value.toLowerCase() === category.toLowerCase()
        )?.labelKey;
        return {
          category,
          label: labelKey ? t(labelKey) : category,
          faqs: items,
        };
      })
      .filter(({ faqs: items }) => items.length > 0);
  }, [filteredFaqs, activeCategory, generalFallback, t]);

  const sidebarLinks = useMemo(
    () => [
      {
        href: buildResourcesPageHref(),
        icon: BookOpen,
        title: t("faq.sidebarLinks.resourcesTitle"),
        description: t("faq.sidebarLinks.resourcesDesc"),
      },
      {
        href: "/contact",
        icon: Mail,
        title: t("faq.sidebarLinks.contactTitle"),
        description: t("faq.sidebarLinks.contactDesc"),
      },
      {
        href: "/contact?subject=suggest-resource",
        icon: MessageCircle,
        title: t("faq.sidebarLinks.suggestTitle"),
        description: t("faq.sidebarLinks.suggestDesc"),
      },
    ],
    [t]
  );

  return (
    <div>
      <PageHeroBand
        icon={HelpCircle}
        title={t("faq.heading")}
        description={t("faq.intro")}
      />

      <div className={cn("app-band-alt", pageSectionPadding)}>
        <div className="mx-auto max-w-6xl">
          <div className="mb-8 space-y-5">
            <SearchField
              label={t("faq.searchLabel")}
              placeholder={t("faq.searchPlaceholder")}
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              aria-controls="faq-results"
            />

            <div
              className="flex flex-wrap gap-2"
              role="tablist"
              aria-label={t("faq.categoryFilterLabel")}
            >
              {categoryFilters.map(({ value, label }) => {
                const isActive = activeCategory === value;
                return (
                  <button
                    key={value}
                    type="button"
                    role="tab"
                    aria-selected={isActive}
                    onClick={() => setActiveCategory(value)}
                    className={cn(
                      "min-h-[44px] cursor-pointer rounded-full px-4 py-2 text-sm font-semibold transition-colors",
                      "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring",
                      isActive
                        ? "bg-primary text-primary-foreground"
                        : "border border-border bg-card text-foreground hover:bg-secondary"
                    )}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)] lg:items-start">
            <div id="faq-results" className="space-y-8">
              {faqs.length === 0 ? (
                <Card className="p-6 sm:p-8">
                  <p className="text-base leading-relaxed text-muted-foreground">{t("faq.empty")}</p>
                </Card>
              ) : grouped.length === 0 ? (
                <Card className="p-6 sm:p-8">
                  <p className="text-base leading-relaxed text-muted-foreground">{t("faq.noResults")}</p>
                </Card>
              ) : (
                grouped.map(({ category, label, faqs: categoryFaqs }) => (
                  <section key={category} aria-labelledby={`faq-section-${category}`}>
                    <h2
                      id={`faq-section-${category}`}
                      className="mb-4 text-xl font-bold text-foreground sm:text-2xl"
                    >
                      {label}
                    </h2>
                    <FaqAccordion faqs={categoryFaqs} />
                  </section>
                ))
              )}
            </div>

            <aside className="space-y-6">
              <Card className="p-6 sm:p-7">
                <h2 className="mb-3 text-lg font-bold text-foreground">{t("faq.stillNeedHelpTitle")}</h2>
                <p className="mb-5 text-base leading-relaxed text-muted-foreground">
                  {t("faq.stillNeedHelpBody")}
                </p>
                <Link
                  href="/contact"
                  className={cn(
                    "inline-flex min-h-[48px] w-full cursor-pointer items-center justify-center gap-2 rounded-xl bg-primary px-6 py-3 text-base font-semibold text-primary-foreground transition-colors",
                    "hover:bg-primary-hover focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
                  )}
                >
                  {t("footer.contactUs")}
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </Link>
              </Card>

              <Card className="p-6 sm:p-7">
                <h2 className="mb-5 text-lg font-bold text-foreground">{t("faq.quickLinksTitle")}</h2>
                <ul className="space-y-5">
                  {sidebarLinks.map(({ href, icon: Icon, title, description }) => (
                    <li key={href}>
                      <Link
                        href={href}
                        className={cn(
                          "group flex items-center gap-4 rounded-xl transition-colors",
                          "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring"
                        )}
                      >
                        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-secondary text-primary">
                          <Icon className="h-5 w-5" aria-hidden="true" />
                        </span>
                        <span>
                          <span className="block font-semibold text-foreground group-hover:text-primary">
                            {title}
                          </span>
                          <span className="mt-0.5 block text-sm leading-relaxed text-muted-foreground">
                            {description}
                          </span>
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </Card>

              <Card className="border-primary/15 bg-secondary/60 p-6 sm:p-7">
                <h2 className="mb-3 text-lg font-bold text-foreground">{t("faq.crisisTitle")}</h2>
                <p className="text-base leading-relaxed text-foreground/90">{t("faq.crisisBody")}</p>
              </Card>
            </aside>
          </div>
        </div>
      </div>

      <section
        className={cn("app-hero-surface", pageSectionPadding)}
        aria-labelledby="faq-cta-heading"
      >
        <div className="mx-auto max-w-3xl text-center">
          <h2 id="faq-cta-heading" className="text-3xl font-bold text-primary-foreground sm:text-4xl">
            {t("faq.ctaTitle")}
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-primary-foreground/90 sm:text-lg">
            {t("faq.ctaSubtitle")}
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href={buildResourcesPageHref()}
              className={cn(
                "inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-xl bg-card px-8 py-3 text-lg font-semibold text-primary transition-colors",
                "hover:bg-card/90 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
              )}
            >
              {t("faq.ctaBrowse")}
              <ArrowRight className="h-5 w-5" aria-hidden="true" />
            </Link>
            <Link
              href="/contact"
              className={cn(
                "inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-xl border-2 border-primary-foreground/40 bg-transparent px-8 py-3 text-lg font-semibold text-primary-foreground transition-colors",
                "hover:bg-primary-foreground/10 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
              )}
            >
              {t("faq.ctaContact")}
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
