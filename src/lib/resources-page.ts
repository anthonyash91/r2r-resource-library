export const RESOURCE_RESULTS_ID = "resource-results";

export const RESOURCE_RESULTS_HASH = `#${RESOURCE_RESULTS_ID}`;

export function buildResourcesPageHref(
  params?: URLSearchParams | Record<string, string | undefined | null>
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

  const qs = searchParams.toString();
  return qs
    ? `/resources?${qs}${RESOURCE_RESULTS_HASH}`
    : `/resources${RESOURCE_RESULTS_HASH}`;
}
