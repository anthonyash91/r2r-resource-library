import { HeroSection } from "@/components/home/hero-section";
import { HomeScrollProgress } from "@/components/home/home-scroll-progress";
import { getServerTranslator } from "@/i18n/server";
import {
  getCategories,
  getResources,
  getHomepageContent,
  getFeaturedResources,
  getAnnouncements,
  getPopularCategoryTags,
} from "@/lib/data";
import { AnnouncementsBanner } from "@/components/home/announcements-banner";
import { FacilityEnterErrorBanner } from "@/components/facility/facility-enter-error-banner";
import { RecommendedResourcesSection } from "@/components/resources/recommended-resources-section";
import { HomeSectionDivider, homeSectionDividerFeaturedClass, homeSectionDividerFlushClass, homeSectionDividerServicesClass } from "@/components/home/home-section-divider";
import { HomeServicesSection } from "@/components/home/home-services-section";
import { HomeFeaturedResourcesSection } from "@/components/home/home-featured-resources-section";
import { HomeHowItWorksSection } from "@/components/home/home-how-it-works-section";
import { HomeDifferentSection } from "@/components/home/home-different-section";
import { HomeCaseWorkerSection } from "@/components/home/home-case-worker-section";
import { HomeGetListedSection } from "@/components/home/home-get-listed-section";
import { HomePossibleSection } from "@/components/home/home-possible-section";
import { HomeAccountComparisonSection } from "@/components/home/home-account-comparison-section";
import { HomeCtaBandSection } from "@/components/home/home-cta-band-section";
import { getRecommendedResources } from "@/lib/user-preferences/recommendations";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ facility_error?: string }>;
}) {
  const { t } = await getServerTranslator();
  const params = await searchParams;

  const categories = await getCategories();

  const [resources, homepage, featuredResources, announcements, preferences, popularTags] =
    await Promise.all([
      getResources(),
      getHomepageContent(),
      getFeaturedResources(),
      getAnnouncements(),
      getServerUserPreferences(),
      getPopularCategoryTags(categories),
    ]);

  const personalized = hasCompletedOnboarding(preferences);
  const recommended = personalized
    ? getRecommendedResources(resources, preferences)
    : [];

  const headline = homepage.hero_headline ?? t("home.heroHeadline");
  const subheadline = homepage.hero_subheadline ?? t("home.heroSubheadline");
  const headlineHighlight = homepage.hero_headline_highlight ?? t("home.heroHighlight");

  const stateCount = new Set(resources.map((r) => r.state).filter(Boolean)).size;
  const resourceStat =
    resources.length >= 100 ? `${resources.length}+` : String(resources.length);

  return (
    <div className="home-page-shell flex flex-col gap-4 overflow-x-hidden sm:gap-6">
      <HomeScrollProgress />
      <FacilityEnterErrorBanner error={params.facility_error} />
      <AnnouncementsBanner announcements={announcements} />

      <HeroSection
        headline={headline}
        subheadline={subheadline}
        highlight={headlineHighlight}
        resourceStat={resourceStat}
        stateCount={stateCount}
        popularTags={popularTags}
      />

      <HomeSectionDivider className={homeSectionDividerServicesClass} />

      <HomeServicesSection />

      <HomeSectionDivider className={homeSectionDividerFeaturedClass} />

      <HomeFeaturedResourcesSection resources={featuredResources} />

      {recommended.length > 0 ? (
        <RecommendedResourcesSection
          resources={recommended}
          county={preferences.county}
          state={preferences.state}
          priorityCategories={preferences.priorityCategories}
          variant="home"
          band="surface"
        />
      ) : null}

      <HomeHowItWorksSection />

      <HomeDifferentSection />

      <HomeSectionDivider className={homeSectionDividerFlushClass} />

      <HomeCaseWorkerSection />

      <HomeSectionDivider className={homeSectionDividerFlushClass} />

      <HomeGetListedSection />

      <HomePossibleSection resources={resources} resourceStat={resourceStat} />

      <HomeAccountComparisonSection />

      <HomeCtaBandSection
        resourceStat={resourceStat}
        stateCount={stateCount}
        categoryCount={categories.length}
      />
    </div>
  );
}
