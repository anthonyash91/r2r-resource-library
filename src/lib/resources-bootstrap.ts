import type { Category, Resource, ResourceFilters } from "@/types";
import {
  getCategories,
  getStates,
  loadActiveResourcePool,
  queryResourcesFromPool,
  resolveZipLocationFromFilters,
} from "@/lib/data";
import {
  buildResourceFilterOptions,
  type ResourceFilterFacetParams,
} from "@/lib/resource-filter-facets";
import { parseIntakeFilterParam } from "@/lib/intake-signals";
import { getRecommendedResources } from "@/lib/user-preferences/recommendations";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";
import {
  resourcesPageQueryWithPreferenceDefaults,
  isResourcesBrowseAllView,
} from "@/lib/resources-page";
import {
  resourcesPageParamsFromSearchParams,
  type ResourcesPageSearchParams,
} from "@/lib/resources-page-filters";
import { resolveResourcesPageFilters } from "@/lib/resources-page-filters.server";
import { getStateCounties } from "@/lib/states/counties";
import type { ZipLocation } from "@/lib/resource-zip-search";
import type { UserPreferences } from "@/lib/user-preferences/types";

export interface ResourcesBootstrapPayload {
  resources: Resource[];
  zipSearch: ZipLocation | null;
  categories: Category[];
  states: string[];
  globalOptions: ReturnType<typeof mapFilterOptions>;
  appliedOptions: ReturnType<typeof mapFilterOptions>;
  recommended: Resource[];
  preferences: {
    county: string | null;
    state: string | null;
    priorityCategories: string[];
  };
  params: ResourcesPageSearchParams;
}

function mapFilterOptions(options: ReturnType<typeof buildResourceFilterOptions>) {
  return {
    cities: options.cities,
    counties: options.counties,
    countyCounts: options.countyCounts,
    services: options.services,
    categories: options.categories,
    categoryCounts: options.categoryCounts,
    serviceCounts: options.serviceCounts,
    intakeCounts: options.intakeCounts,
  };
}

export function resolveEffectiveResourcesPageParams(
  urlParams: ResourcesPageSearchParams,
  preferences: UserPreferences
): ResourcesPageSearchParams {
  const query = resourcesPageQueryWithPreferenceDefaults(urlParams, preferences);
  if (!query) return urlParams;
  return resourcesPageParamsFromSearchParams(new URLSearchParams(query));
}

function resolveBootstrapPoolState(
  params: ResourcesPageSearchParams,
  filters: ResourceFilters,
  zipSearch: ZipLocation | null,
  preferences: UserPreferences
): string | undefined {
  const fromFilters = filters.state?.trim() || zipSearch?.state;
  if (fromFilters) return fromFilters;
  if (isResourcesBrowseAllView(params as Partial<Record<string, string | undefined>>)) {
    return undefined;
  }
  if (params.state?.trim()) return params.state.trim();
  if (hasCompletedOnboarding(preferences) && preferences.state?.trim()) {
    return preferences.state.trim();
  }
  return undefined;
}

async function buildFacetOptions(
  pool: Resource[],
  categories: Category[],
  params: ResourceFilterFacetParams
) {
  let categoryId = params.categoryId;
  if (!categoryId && params.categorySlug) {
    categoryId = categories.find((category) => category.slug === params.categorySlug)?.id;
  }

  const resolvedParams: ResourceFilterFacetParams = {
    ...params,
    categoryId,
  };
  const stateCounties = params.state ? [...getStateCounties(params.state)] : [];
  return buildResourceFilterOptions(pool, categories, resolvedParams, stateCounties);
}

export async function getResourcesBootstrap(
  params: ResourcesPageSearchParams
): Promise<ResourcesBootstrapPayload> {
  const [filters, preferences, categories, states] = await Promise.all([
    resolveResourcesPageFilters(params),
    getServerUserPreferences(),
    getCategories(),
    getStates(),
  ]);

  const zipSearch = resolveZipLocationFromFilters(filters);
  const poolState = resolveBootstrapPoolState(params, filters, zipSearch, preferences);
  const resourcePool = await loadActiveResourcePool(poolState);

  const queryResult = await queryResourcesFromPool(resourcePool, filters);

  const globalOptions = await buildFacetOptions(resourcePool, categories, {
    state: poolState,
  });

  const appliedOptions = await buildFacetOptions(resourcePool, categories, {
    state: params.state ?? zipSearch?.state ?? poolState,
    county: params.county,
    city: params.city,
    categorySlug: params.category,
    service: params.service,
    intake: parseIntakeFilterParam(params.intake),
  });

  const personalized = hasCompletedOnboarding(preferences);
  const recommended = personalized
    ? getRecommendedResources(resourcePool, preferences)
    : [];

  return {
    resources: queryResult.resources,
    zipSearch: queryResult.zipSearch,
    categories,
    states,
    globalOptions: mapFilterOptions(globalOptions),
    appliedOptions: mapFilterOptions(appliedOptions),
    recommended,
    preferences: {
      county: preferences.county,
      state: preferences.state,
      priorityCategories: preferences.priorityCategories,
    },
    params,
  };
}

export function searchParamsFromPageProps(
  raw: Record<string, string | string[] | undefined>
): URLSearchParams {
  const searchParams = new URLSearchParams();
  for (const [key, value] of Object.entries(raw)) {
    if (Array.isArray(value)) {
      for (const item of value) {
        if (item) searchParams.append(key, item);
      }
    } else if (value) {
      searchParams.set(key, value);
    }
  }
  return searchParams;
}
