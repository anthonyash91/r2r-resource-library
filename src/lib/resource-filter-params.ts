export const RESOURCE_FILTER_PARAM_KEYS = [
  "q",
  "zip",
  "category",
  "county",
  "state",
  "city",
  "service",
  "tag",
  "coverage",
  "intake",
  "filter",
] as const;

export type ResourceFilterParamKey = (typeof RESOURCE_FILTER_PARAM_KEYS)[number];

export function hasActiveResourceFilters(
  searchParams: URLSearchParams | Pick<URLSearchParams, "get">
): boolean {
  return RESOURCE_FILTER_PARAM_KEYS.some((key) => {
    const value = searchParams.get(key);
    return value != null && value.trim() !== "";
  });
}

export function hasActiveResourceFiltersFromParams(
  params: Partial<Record<ResourceFilterParamKey, string | undefined>>
): boolean {
  return RESOURCE_FILTER_PARAM_KEYS.some((key) => {
    const value = params[key];
    return value != null && value.trim() !== "";
  });
}
