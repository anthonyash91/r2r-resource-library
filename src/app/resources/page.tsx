import { Suspense } from "react";
import type { Metadata } from "next";
import { ResourcesHeroSection } from "@/components/home/hero-section";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { ResourceResultsSummary } from "@/components/resources/resource-results-summary";
import { ResourceFiltersPanel } from "@/components/resources/resource-filters-panel";
import { getServerTranslator } from "@/i18n/server";
import { cn, sectionStackGap } from "@/lib/utils";
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
    recentlyAdded: params.filter === "recent",
  };

  const [resources, categories, states, counties, cities, services] =
    await Promise.all([
      getResources(filters),
      getCategories(),
      getStates(),
      getCounties(params.state),
      getCities(params.state, params.county),
      getServices(),
    ]);

  return (
    <>
      <Suspense fallback={<div className="h-48 animate-pulse bg-primary" aria-hidden="true" />}>
        <ResourcesHeroSection />
      </Suspense>

      <div className="px-4 pb-8 pt-6 sm:px-6 lg:px-8">
        <div className={cn("mx-auto max-w-7xl", sectionStackGap)}>
          <Suspense fallback={<div className="h-12 animate-pulse rounded-xl bg-muted" />}>
            <ResourceFiltersPanel
              categories={categories}
              states={states}
              counties={counties}
              cities={cities}
              services={services}
            />
          </Suspense>

          {resources.length === 0 ? (
            <div className="rounded-xl border border-border bg-card p-12 text-center">
              <h2 className="mb-2 text-xl font-bold">{t("resources.noResults")}</h2>
              <p className="text-base text-muted-foreground">{t("resources.noResultsHint")}</p>
            </div>
          ) : (
            <>
              <ResourceResultsSummary
                count={resources.length}
                label={t("resources.resultsSummary")}
              />
              <ResourceMasonry resources={resources} />
            </>
          )}
        </div>
      </div>
    </>
  );
}
