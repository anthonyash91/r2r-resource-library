import { NextResponse } from "next/server";
import {
  getResources,
  getCategories,
  getStates,
  getResourceFilterOptions,
} from "@/lib/data";
import { parseIntakeFilterParam } from "@/lib/intake-signals";
import { getRecommendedResources } from "@/lib/user-preferences/recommendations";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";
import {
  resourcesPageParamsFromSearchParams,
  type ResourcesPageSearchParams,
} from "@/lib/resources-page-filters";
import { resolveResourcesPageFilters } from "@/lib/resources-page-filters.server";

function mapFilterOptions(options: Awaited<ReturnType<typeof getResourceFilterOptions>>) {
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

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const params: ResourcesPageSearchParams = resourcesPageParamsFromSearchParams(searchParams);
  const filters = await resolveResourcesPageFilters(params);
  const preferences = await getServerUserPreferences();

  const [resources, categories, states, globalFilterOptions, appliedFilterOptions, allResources] =
    await Promise.all([
      getResources(filters),
      getCategories(),
      getStates(),
      getResourceFilterOptions(),
      getResourceFilterOptions({
        state: params.state,
        county: params.county,
        city: params.city,
        categorySlug: params.category,
        service: params.service,
        intake: parseIntakeFilterParam(params.intake),
      }),
      getResources(),
    ]);

  const personalized = hasCompletedOnboarding(preferences);
  const recommended = personalized
    ? getRecommendedResources(allResources, preferences)
    : [];

  return NextResponse.json({
    resources,
    categories,
    states,
    globalOptions: mapFilterOptions(globalFilterOptions),
    appliedOptions: mapFilterOptions(appliedFilterOptions),
    recommended,
    preferences: {
      county: preferences.county,
      state: preferences.state,
      priorityCategories: preferences.priorityCategories,
    },
    params,
  });
}
