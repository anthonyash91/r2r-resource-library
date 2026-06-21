import { Suspense } from "react";
import type { Metadata } from "next";
import { ResourcesHeroSection } from "@/components/home/hero-section";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { ResourceResultsSummary } from "@/components/resources/resource-results-summary";
import { CountyFilteredResourceResults } from "@/components/resources/county-filtered-resource-results";
import { ResourceFiltersPanel } from "@/components/resources/resource-filters-panel";
import { ScrollToResourceResults } from "@/components/resources/scroll-to-resource-results";
import { RESOURCE_RESULTS_ID } from "@/lib/resources-page";
import { getServerTranslator } from "@/i18n/server";
import { cn, pageSectionPadding, sectionStackGap } from "@/lib/utils";
import { isValidCoverage, partitionResourcesByCountyFilter } from "@/lib/resource-coverage";
import { hasActiveResourceFiltersFromParams } from "@/lib/resource-filter-params";
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
    filter?: string;
  }>;
}

export default async function ResourcesPage({ searchParams }: PageProps) {
  const { t } = await getServerTranslator();
  const params = await searchParams;

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
    recentlyAdded: params.filter === "recent",
  };

  const [resources, categories, states, counties, cities, services] =
    await Promise.all([
      getResources(filters),
      getCategories(),
      getStates(),
      getCounties(params.state ?? "Kentucky"),
      getCities(params.state, params.county),
      getServices(),
    ]);

  const searchQuery = params.q?.trim();
  const selectedCounty = params.county?.trim();
  const showCountySplit = Boolean(selectedCounty) && filters.coverage !== "statewide";
  const resultsSummaryLabel = searchQuery
    ? t("resources.resultsSummaryWithQuery", { query: searchQuery })
    : t("resources.resultsSummary");
  const { local: localResults, statewide: statewideResults } = showCountySplit
    ? partitionResourcesByCountyFilter(resources, selectedCounty)
    : { local: resources, statewide: [] as typeof resources };

  const filtersPanelOpen = hasActiveResourceFiltersFromParams(params);

  return (
    <>
      <Suspense fallback={<div className="h-48 animate-pulse bg-primary" aria-hidden="true" />}>
        <ResourcesHeroSection />
      </Suspense>

      <div className={cn("app-band-alt", pageSectionPadding)}>
        <div className={cn("mx-auto max-w-7xl", sectionStackGap)}>
          <Suspense fallback={null}>
            <ScrollToResourceResults />
          </Suspense>

          <Suspense fallback={<div className="h-12 animate-pulse rounded-xl bg-muted" />}>
            <ResourceFiltersPanel
              defaultOpen={filtersPanelOpen}
              categories={categories}
              states={states}
              counties={counties}
              cities={cities}
              services={services}
            />
          </Suspense>

          <div
            id={RESOURCE_RESULTS_ID}
            className={cn("scroll-mt-[var(--site-header-height)]", sectionStackGap)}
          >
          {resources.length === 0 ? (
            <div className="rounded-xl border border-border bg-card p-12 text-center">
              <h2 className="mb-2 text-xl font-bold">{t("resources.noResults")}</h2>
              <p className="text-base text-muted-foreground">{t("resources.noResultsHint")}</p>
            </div>
          ) : showCountySplit ? (
            <CountyFilteredResourceResults
              county={selectedCounty!}
              local={localResults}
              statewide={statewideResults}
              summaryLabel={t("resources.resultsSplitSummary", {
                local: localResults.length,
                statewide: statewideResults.length,
                county: selectedCounty!,
              })}
              inCountyHeading={t("resources.resultsInCountyHeading", {
                county: selectedCounty!,
              })}
              inCountyHint={t("resources.resultsInCountyHint", {
                county: selectedCounty!,
              })}
              statewideHeading={t("resources.resultsStatewideHeading")}
              statewideHint={t("resources.resultsStatewideHint", {
                county: selectedCounty!,
              })}
              noLocalHint={
                localResults.length === 0
                  ? t("resources.resultsNoLocalInCounty", { county: selectedCounty! })
                  : undefined
              }
            />
          ) : (
            <>
              <ResourceResultsSummary
                count={resources.length}
                label={resultsSummaryLabel}
              />
              <ResourceMasonry resources={resources} />
            </>
          )}
          </div>
        </div>
      </div>
    </>
  );
}
