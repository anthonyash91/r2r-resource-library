import Link from "next/link";
import { Search, Bookmark, Handshake, ArrowRight, CircleCheck } from "lucide-react";
import { HeroSection } from "@/components/home/hero-section";
import { CategoryPills } from "@/components/resources/category-pills";
import { FeaturedResourcesSection } from "@/components/resources/featured-resources-section";
import { getServerTranslator } from "@/i18n/server";
import {
  getCategories,
  getResources,
  getHomepageContent,
} from "@/lib/data";

const POPULAR_TAG_SLUGS = [
  "housing",
  "employment",
  "healthcare",
  "legal-aid",
  "mental-health",
  "substance-abuse-recovery",
] as const;

export default async function HomePage() {
  const { t } = await getServerTranslator();

  const [categories, resources, homepage] = await Promise.all([
    getCategories(),
    getResources(),
    getHomepageContent(),
  ]);

  const headline = homepage.hero_headline ?? t("home.heroHeadline");
  const subheadline = homepage.hero_subheadline ?? t("home.heroSubheadline");
  const headlineHighlight = homepage.hero_headline_highlight ?? t("home.heroHighlight");

  const popularTags = POPULAR_TAG_SLUGS.flatMap((slug) => {
    const category = categories.find((item) => item.slug === slug);
    if (!category) return [];
    const label = t(`categories.${slug}.shortName`);
    return [{ label, slug }];
  });

  const stateCount = new Set(resources.map((r) => r.state).filter(Boolean)).size;
  const resourceStat =
    resources.length >= 100 ? `${resources.length}+` : String(resources.length);

  const howItWorksSteps = [
    {
      step: "1",
      title: t("home.stepSearchTitle"),
      description: t("home.stepSearchDesc"),
      icon: Search,
    },
    {
      step: "2",
      title: t("home.stepSaveTitle"),
      description: t("home.stepSaveDesc"),
      icon: Bookmark,
    },
    {
      step: "3",
      title: t("home.stepConnectTitle"),
      description: t("home.stepConnectDesc"),
      icon: Handshake,
    },
  ];

  const builtForFeatures = [
    t("home.builtForFeature1"),
    t("home.builtForFeature2"),
    t("home.builtForFeature3"),
    t("home.builtForFeature4"),
  ];

  const statCards = [
    { value: resourceStat, label: t("home.statResources") },
    { value: String(stateCount), label: t("home.statStates") },
    { value: String(categories.length), label: t("home.statCategories") },
    { value: "100%", label: t("home.statFree") },
  ];

  return (
    <>
      <HeroSection
        headline={headline}
        subheadline={subheadline}
        highlight={headlineHighlight}
        resourceStat={resourceStat}
        stateCount={stateCount}
        popularTags={popularTags}
      />

      <section className="px-4 py-16 sm:px-6 lg:px-8 lg:py-20" aria-labelledby="categories-heading">
        <div className="mx-auto max-w-7xl">
          <header className="mb-10 text-center">
            <h2 id="categories-heading" className="text-3xl font-bold sm:text-4xl">
              {t("home.browseByCategoryTitle")}
            </h2>
            <p className="mt-1 text-base text-muted-foreground">
              {t("home.browseByCategorySubtitle")}
            </p>
          </header>

          <CategoryPills categories={categories} compact wrap />
        </div>
      </section>

      <section
        id="how-it-works-heading"
        className="bg-muted px-4 py-16 sm:px-6 lg:px-8 lg:py-20"
        aria-labelledby="how-it-works-title"
      >
        <div className="mx-auto max-w-6xl">
          <header className="mb-14 text-center">
            <h2 id="how-it-works-title" className="mb-3 text-3xl font-bold text-foreground sm:text-4xl">
              {t("home.howItWorksTitle")}
            </h2>
            <p className="text-lg text-muted-foreground">{t("home.howItWorksSubtitle")}</p>
          </header>

          <div className="grid gap-12 md:grid-cols-3 md:gap-8 lg:gap-12">
            {howItWorksSteps.map(({ step, title, description, icon: Icon }) => (
              <div key={step} className="text-center">
                <div className="relative mx-auto mb-6 inline-flex">
                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary shadow-sm sm:h-[4.5rem] sm:w-[4.5rem]">
                    <Icon className="h-7 w-7 text-primary-foreground sm:h-8 sm:w-8" aria-hidden="true" />
                  </div>
                  <span className="absolute -right-2 -top-2 flex h-7 w-7 items-center justify-center rounded-full bg-accent text-sm font-bold text-accent-foreground shadow-sm ring-2 ring-muted">
                    {step}
                  </span>
                </div>
                <h3 className="mb-3 text-xl font-bold text-foreground">{title}</h3>
                <p className="mx-auto max-w-xs text-base leading-relaxed text-muted-foreground">
                  {description}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-14 text-center">
            <Link
              href="/resources"
              className="inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-xl bg-primary px-8 py-3 text-lg font-semibold text-primary-foreground transition-colors hover:bg-primary-hover focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
            >
              {t("home.startSearching")}
              <ArrowRight className="h-5 w-5" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>

      <FeaturedResourcesSection resources={resources} />

      <section
        className="bg-gradient-to-br from-primary via-primary-hover to-accent px-4 py-16 sm:px-6 lg:px-8 lg:py-20"
        aria-labelledby="built-for-heading"
      >
        <div className="mx-auto grid max-w-6xl items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <div>
            <h2
              id="built-for-heading"
              className="mb-4 text-3xl font-bold text-primary-foreground sm:text-4xl"
            >
              {t("home.builtForTitle")}
            </h2>
            <p className="mb-8 text-lg leading-relaxed text-primary-foreground/90">
              {t("home.builtForDesc")}
            </p>
            <ul className="mb-10 space-y-4">
              {builtForFeatures.map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <CircleCheck
                    className="mt-0.5 h-5 w-5 shrink-0 text-secondary"
                    aria-hidden="true"
                  />
                  <span className="text-base text-primary-foreground/90">{item}</span>
                </li>
              ))}
            </ul>
            <div className="flex flex-wrap gap-4">
              <Link
                href="/signup"
                className="inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-full bg-card px-8 py-3 text-lg font-semibold text-primary transition-colors hover:bg-card/90 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
              >
                {t("home.createFreeAccount")}
                <ArrowRight className="h-5 w-5" aria-hidden="true" />
              </Link>
              <Link
                href="/resources"
                className="inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-full border-2 border-primary-foreground/40 bg-transparent px-8 py-3 text-lg font-semibold text-primary-foreground transition-colors hover:bg-primary-foreground/10 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
              >
                {t("home.browseResources")}
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 sm:gap-5">
            {statCards.map(({ value, label }) => (
              <div
                key={label}
                className="rounded-2xl border border-primary-foreground/15 bg-primary-foreground/10 px-4 py-8 text-center backdrop-blur-sm sm:px-6 sm:py-10"
              >
                <p className="text-3xl font-bold text-primary-foreground sm:text-4xl">{value}</p>
                <p className="mt-2 text-sm font-medium text-primary-foreground/75 sm:text-base">
                  {label}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
