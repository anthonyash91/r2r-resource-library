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

/** Query param consumed by ScrollToResourceResults (avoids fragile URL hash handling). */
export const RESOURCES_PAGE_SCROLL_PARAM = "scroll";

export type ResourcesPageScrollTarget = "results" | "recommended" | "none";

/**
 * Scroll intent for `/resources` links (via `?scroll=`, consumed by ScrollToResourceResults):
 * - `none` — land at the hero/search (nav Find Resources, generic “browse”, empty search).
 * - `results` — scroll to the filtered results block (search, filters, badges, county browse).
 * - `recommended` — scroll to the picked-for-you section (onboarding finish).
 *
 * Preference auto-redirect on bare `/resources` never adds `scroll`, so nav stays at the top.
 */
export function parseResourcesPageScrollTarget(
  searchParams: URLSearchParams | Pick<URLSearchParams, "get">,
  hash = ""
): ResourcesPageScrollTarget {
  const scroll = searchParams.get(RESOURCES_PAGE_SCROLL_PARAM);
  if (scroll === "recommended" || hash === RECOMMENDED_RESOURCES_HASH) return "recommended";
  if (
    scroll === "results" ||
    hash === RESOURCE_RESULTS_HASH ||
    hash.startsWith(`${RESOURCE_RESULTS_HASH}#`)
  ) {
    return "results";
  }
  return "none";
}

/** When set, skip onboarding preference auto-redirect (explicit browse-all / cleared filters). */
export const RESOURCES_BROWSE_PARAM = "browse";

export function isResourcesBrowseAllView(
  params: Partial<Record<string, string | undefined>>
): boolean {
  return params[RESOURCES_BROWSE_PARAM] === "1";
}

export function buildResourcesPageClearedHref(): string {
  const searchParams = new URLSearchParams();
  searchParams.set(RESOURCES_BROWSE_PARAM, "1");
  return `/resources?${searchParams.toString()}`;
}

export function resourcesPageQueryWithPreferenceDefaults(
  params: Partial<Record<ResourceFilterParamKey | typeof RESOURCES_BROWSE_PARAM, string | undefined>>,
  preferences: UserPreferences
): string | null {
  if (isResourcesBrowseAllView(params)) return null;
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
  scrollTo: ResourcesPageScrollTarget = "none"
): string {
  const searchParams = new URLSearchParams();

  if (params instanceof URLSearchParams) {
    params.forEach((value, key) => {
      if (key === RESOURCES_PAGE_SCROLL_PARAM) return;
      if (value.trim()) {
        searchParams.set(key, value);
      }
    });
  } else if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (key === RESOURCES_PAGE_SCROLL_PARAM) continue;
      if (value?.trim()) {
        searchParams.set(key, value.trim());
      }
    }
  }

  if (scrollTo === "recommended") {
    searchParams.set(RESOURCES_PAGE_SCROLL_PARAM, "recommended");
  } else if (scrollTo === "results") {
    searchParams.set(RESOURCES_PAGE_SCROLL_PARAM, "results");
  }

  const qs = searchParams.toString();
  return qs ? `/resources?${qs}` : "/resources";
}
