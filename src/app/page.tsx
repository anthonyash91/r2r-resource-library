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
  getFeaturedResources,
  getAnnouncements,
} from "@/lib/data";
import { AnnouncementsBanner } from "@/components/home/announcements-banner";
import { FacilitySessionBar } from "@/components/facility/facility-session-bar";
import { RecommendedResourcesSection } from "@/components/resources/recommended-resources-section";
import { HeroSurfaceOrbs } from "@/components/layout/hero-surface-orbs";
import { cn, pageSectionPadding, checkIconClass, pageSectionHeadingClass, pageSectionSubtitleClass, pageSectionSubtitleOnHeroClass, pageSectionSubheadingClass } from "@/lib/utils";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { getRecommendedResources } from "@/lib/user-preferences/recommendations";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";

const POPULAR_TAG_SLUGS = [
  "housing",
  "employment",
  "healthcare",
  "legal-aid",
  "substance-use-treatment",
  "basic-needs",
] as const;

export default async function HomePage() {
  const { t } = await getServerTranslator();

  const [categories, resources, homepage, featuredResources, announcements, preferences] =
    await Promise.all([
    getCategories(),
    getResources(),
    getHomepageContent(),
    getFeaturedResources(),
    getAnnouncements(),
    getServerUserPreferences(),
  ]);

  const personalized = hasCompletedOnboarding(preferences);
  const recommended = personalized
    ? getRecommendedResources(resources, preferences)
    : [];

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

  const showRecommended = recommended.length > 0;

  return (
    <>
      <AnnouncementsBanner announcements={announcements} />
      <FacilitySessionBar />

      <HeroSection
        headline={headline}
        subheadline={subheadline}
        highlight={headlineHighlight}
        resourceStat={resourceStat}
        stateCount={stateCount}
        popularTags={popularTags}
      />

      <section
        className={cn(showRecommended ? "bg-card" : "app-band-muted", pageSectionPadding)}
        aria-labelledby="categories-heading"
      >
        <div className="mx-auto max-w-7xl">
          <header className="mb-10 text-center">
            <h2 id="categories-heading" className={pageSectionHeadingClass}>
              {t("home.browseByCategoryTitle")}
            </h2>
            <p className={cn("mt-1", pageSectionSubtitleClass)}>
              {t("home.browseByCategorySubtitle")}
            </p>
          </header>

          <CategoryPills
            categories={categories}
            compact
            wrap
            size="lg"
            highlightAllWhenUnset={false}
          />
        </div>
      </section>

      {recommended.length > 0 ? (
        <RecommendedResourcesSection
          resources={recommended}
          county={preferences.county}
          state={preferences.state}
          priorityCategories={preferences.priorityCategories}
          variant="home"
        />
      ) : null}

      <section
        id="how-it-works-heading"
        className={cn("bg-card", pageSectionPadding)}
        aria-labelledby="how-it-works-title"
      >
        <div className="mx-auto max-w-6xl">
          <header className="mb-14 text-center">
            <h2 id="how-it-works-title" className={cn("mb-3 text-foreground", pageSectionHeadingClass)}>
              {t("home.howItWorksTitle")}
            </h2>
            <p className={pageSectionSubtitleClass}>{t("home.howItWorksSubtitle")}</p>
          </header>

          <div className="grid gap-12 md:grid-cols-3 md:gap-8 lg:gap-12">
            {howItWorksSteps.map(({ step, title, description, icon: Icon }) => (
              <div key={step} className="text-center">
                <div className="relative mx-auto mb-6 inline-flex">
                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary shadow-sm sm:h-[4.5rem] sm:w-[4.5rem]">
                    <Icon className="h-7 w-7 text-primary-foreground sm:h-8 sm:w-8" aria-hidden="true" />
                  </div>
                  <span className="how-it-works-step-number absolute -right-2 -top-2 flex h-7 w-7 items-center justify-center rounded-full text-sm font-bold shadow-sm ring-2 ring-muted">
                    {step}
                  </span>
                </div>
                <h3 className={cn("mb-3", pageSectionSubheadingClass)}>{title}</h3>
                <p className="mx-auto max-w-xs text-base leading-relaxed text-muted-foreground">
                  {description}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-14 text-center">
            <Link
              href={buildResourcesPageHref()}
              className="inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-xl bg-primary px-8 py-3 text-lg font-semibold text-primary-foreground transition-colors hover:bg-primary-hover focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
            >
              {t("home.startSearching")}
              <ArrowRight className="h-5 w-5" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>

      <FeaturedResourcesSection resources={featuredResources} />

      <section
        className={cn("app-hero-surface relative overflow-hidden", pageSectionPadding)}
        aria-labelledby="built-for-heading"
      >
        <HeroSurfaceOrbs />
        <div className="relative mx-auto grid max-w-6xl items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <div>
            <h2
              id="built-for-heading"
              className={cn("mb-4 text-primary-foreground", pageSectionHeadingClass)}
            >
              {t("home.builtForTitle")}
            </h2>
            <p className={cn("mb-8", pageSectionSubtitleOnHeroClass)}>
              {t("home.builtForDesc")}
            </p>
            <ul className="mb-10 space-y-4">
              {builtForFeatures.map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <CircleCheck
                    className={cn("h-5 w-5 shrink-0", checkIconClass)}
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
                href={buildResourcesPageHref()}
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
