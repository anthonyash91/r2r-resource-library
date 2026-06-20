import { Suspense } from "react";
import type { Metadata } from "next";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { CategoryPills } from "@/components/resources/category-pills";
import { ResourceFiltersPanel } from "@/components/resources/resource-filters-panel";
import { getServerTranslator } from "@/i18n/server";
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
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-6">
          <h1 className="mb-1 text-3xl font-bold sm:text-4xl">{t("resources.findResources")}</h1>
          <p className="text-base text-muted-foreground">
            {t("resources.programCount", { count: resources.length })}
          </p>
        </header>

        <Suspense fallback={<div className="mb-6 h-10 animate-pulse rounded-full bg-muted" />}>
          <CategoryPills categories={categories} preserveParams className="mb-6" />
        </Suspense>

        <Suspense fallback={<div className="mb-6 h-12 animate-pulse rounded-2xl bg-muted" />}>
          <ResourceFiltersPanel
            categories={categories}
            states={states}
            counties={counties}
            cities={cities}
            services={services}
          />
        </Suspense>

        <div className="mt-8">
          {resources.length === 0 ? (
            <div className="rounded-2xl border border-border bg-card p-12 text-center">
              <h2 className="mb-2 text-xl font-bold">{t("resources.noResults")}</h2>
              <p className="text-base text-muted-foreground">{t("resources.noResultsHint")}</p>
            </div>
          ) : (
            <ResourceMasonry resources={resources} />
          )}
        </div>
      </div>
    </div>
  );
}
