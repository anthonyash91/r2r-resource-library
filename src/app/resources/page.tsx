import { Suspense } from "react";
import { redirect } from "next/navigation";
import type { Metadata } from "next";
import { ResourcesHeroSection } from "@/components/home/hero-section";
import { ResourcesPageSkeleton } from "@/components/resources/resources-page-skeleton";
import { PaginatedResourceList } from "@/components/resources/paginated-resource-list";
import { ResourceResultsSection } from "@/components/resources/resource-results-summary";
import { CountyFilteredResourceResults } from "@/components/resources/county-filtered-resource-results";
import { ScrollToResourceResults } from "@/components/resources/scroll-to-resource-results";
import { RESOURCE_RESULTS_ID, resourcesPageQueryWithPreferenceDefaults } from "@/lib/resources-page";
import { parseIntakeFilterParam } from "@/lib/intake-signals";
import { getServerTranslator } from "@/i18n/server";
import { cn, pageSectionPadding, sectionDividerTop, sectionStackGap } from "@/lib/utils";
import { isValidCoverage, partitionResourcesByCountyFilter } from "@/lib/resource-coverage";
import { RecommendedResourcesSection } from "@/components/resources/recommended-resources-section";
import { getRecommendedResources } from "@/lib/user-preferences/recommendations";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";
import {
  getResources,
  getCategories,
  getStates,
  getCounties,
  getCities,
  getServices,
  getCategoryBySlug,
} from "@/lib/data";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("resources.findResources"),
    description: t("resources.metadataDescription"),
  };
}

interface PageProps {
  searchParams: Promise<{
    q?: string;
    state?: string;
    county?: string;
    city?: string;
    category?: string;
    service?: string;
    tag?: string;
    coverage?: string;
    intake?: string;
    filter?: string;
  }>;
}

export default async function ResourcesPage({ searchParams }: PageProps) {
  const { t } = await getServerTranslator();
  const params = await searchParams;

  const preferences = await getServerUserPreferences();
  const defaultQuery = resourcesPageQueryWithPreferenceDefaults(params, preferences);
  if (defaultQuery !== null) {
    redirect(`/resources?${defaultQuery}`);
  }

  let categoryId = params.category;
  if (params.category) {
    const cat = await getCategoryBySlug(params.category);
    if (cat) categoryId = cat.id;
  }

  const filters = {
    query: params.q,
    state: params.state,
    county: params.county,
    city: params.city,
    category: categoryId,
    service: params.service,
    tag: params.tag,
    coverage:
      params.coverage && isValidCoverage(params.coverage)
        ? params.coverage
        : undefined,
    intake: parseIntakeFilterParam(params.intake),
    recentlyAdded: params.filter === "recent",
  };

  const [resources, categories, states, counties, cities, services, allResources] =
    await Promise.all([
      getResources(filters),
      getCategories(),
      getStates(),
      getCounties(params.state ?? "Kentucky"),
      getCities(params.state, params.county),
      getServices(),
      getResources(),
    ]);

  const personalized = hasCompletedOnboarding(preferences);
  const recommended = personalized
    ? getRecommendedResources(allResources, preferences)
    : [];

  const searchQuery = params.q?.trim();
  const selectedCounty = params.county?.trim();
  const showCountySplit = Boolean(selectedCounty) && filters.coverage !== "statewide";
  const resultsHeading = searchQuery
    ? t("resources.resultsSummaryWithQuery", { query: searchQuery })
    : t("resources.resultsSummary");
  const resultsHint = searchQuery
    ? t("resources.resultsHintWithQuery", { query: searchQuery })
    : t("resources.resultsHint");
  const { local: localResults, statewide: statewideResults } = showCountySplit
    ? partitionResourcesByCountyFilter(resources, selectedCounty)
    : { local: resources, statewide: [] as typeof resources };

  return (
    <>
      <Suspense fallback={<ResourcesPageSkeleton loadingLabel={t("resources.loadingAria")} />}>
        <ResourcesHeroSection
          categories={categories}
          states={states}
          counties={counties}
          cities={cities}
          services={services}
        />
      </Suspense>

      <div className={cn("app-band-alt", pageSectionPadding)}>
        <div className={cn("mx-auto max-w-7xl", sectionStackGap)}>
          <Suspense fallback={null}>
            <ScrollToResourceResults />
          </Suspense>

          {recommended.length > 0 ? (
            <RecommendedResourcesSection
              resources={recommended}
              county={preferences.county}
              state={preferences.state}
              priorityCategories={preferences.priorityCategories}
              variant="resources"
            />
          ) : null}

          <div
            id={RESOURCE_RESULTS_ID}
            className={cn(
              "scroll-mt-[var(--site-header-height)]",
              sectionStackGap,
              recommended.length > 0 && sectionDividerTop
            )}
          >
          {resources.length === 0 ? (
            <div className="rounded-xl border border-border bg-card p-12 text-center">
              <h2 className="mb-2 text-xl font-bold">{t("resources.noResults")}</h2>
              <p className="text-base text-muted-foreground">{t("resources.noResultsHint")}</p>
            </div>
          ) : showCountySplit ? (
            <CountyFilteredResourceResults
              local={localResults}
              statewide={statewideResults}
              inCountyHeading={t("resources.resultsInCountyHeading", {
                county: selectedCounty!,
              })}
              inCountyHint={t("resources.resultsInCountyHint", {
                county: selectedCounty!,
              })}
              statewideHeading={t("resources.resultsStatewideHeading")}
              statewideHint={t("resources.resultsStatewideHint", {
                county: selectedCounty!,
                state: params.state?.trim() || "Kentucky",
              })}
              noLocalHint={
                localResults.length === 0
                  ? t("resources.resultsNoLocalInCounty", { county: selectedCounty! })
                  : undefined
              }
            />
          ) : (
            <ResourceResultsSection
              heading={resultsHeading}
              hint={resultsHint}
              count={resources.length}
            >
              <PaginatedResourceList resources={resources} />
            </ResourceResultsSection>
          )}
          </div>
        </div>
      </div>
    </>
  );
}
