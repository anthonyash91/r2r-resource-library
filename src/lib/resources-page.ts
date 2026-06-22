import {
  RESOURCE_FILTER_PARAM_KEYS,
  type ResourceFilterParamKey,
} from "@/lib/resource-filter-params";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";
import type { UserPreferences } from "@/lib/user-preferences/types";

export const RESOURCE_RESULTS_ID = "resource-results";

export const RESOURCE_RESULTS_HASH = `#${RESOURCE_RESULTS_ID}`;

export const RECOMMENDED_RESOURCES_ID = "recommended-resources";

export const RECOMMENDED_RESOURCES_HASH = `#${RECOMMENDED_RESOURCES_ID}`;

export type ResourcesPageScrollTarget = "results" | "recommended" | "none";

export function resourcesPageQueryWithPreferenceDefaults(
  params: Partial<Record<ResourceFilterParamKey, string | undefined>>,
  preferences: UserPreferences
): string | null {
  if (params.state?.trim()) return null;
  if (!hasCompletedOnboarding(preferences) || !preferences.state) return null;

  const searchParams = new URLSearchParams();
  for (const key of RESOURCE_FILTER_PARAM_KEYS) {
    const value = params[key];
    if (value?.trim()) searchParams.set(key, value.trim());
  }
  searchParams.set("state", preferences.state);
  return searchParams.toString();
}

export function buildResourcesPageHref(
  params?: URLSearchParams | Record<string, string | undefined | null>,
  scrollTo: ResourcesPageScrollTarget = "results"
): string {
  const searchParams = new URLSearchParams();

  if (params instanceof URLSearchParams) {
    params.forEach((value, key) => {
      if (value.trim()) {
        searchParams.set(key, value);
      }
    });
  } else if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value?.trim()) {
        searchParams.set(key, value.trim());
      }
    }
  }

  const hash =
    scrollTo === "recommended"
      ? RECOMMENDED_RESOURCES_HASH
      : scrollTo === "none"
        ? ""
        : RESOURCE_RESULTS_HASH;

  const qs = searchParams.toString();
  return qs ? `/resources?${qs}${hash}` : `/resources${hash}`;
}
