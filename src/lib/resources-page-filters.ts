import { parseIntakeFilterParam } from "@/lib/intake-signals";
import { isValidCoverage } from "@/lib/resource-coverage";
import { RESOURCES_BROWSE_PARAM, RESOURCES_PAGE_SCROLL_PARAM } from "@/lib/resources-page";

export interface ResourcesPageSearchParams {
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
  browse?: string;
  scroll?: string;
}

export function resourcesPageParamsFromSearchParams(
  searchParams: URLSearchParams
): ResourcesPageSearchParams {
  const params: ResourcesPageSearchParams = {};
  for (const [key, value] of searchParams.entries()) {
    if (key === RESOURCES_BROWSE_PARAM || key === RESOURCES_PAGE_SCROLL_PARAM) continue;
    (params as Record<string, string>)[key] = value;
  }
  return params;
}

export function resourcesPageParamsKey(params: ResourcesPageSearchParams): string {
  return JSON.stringify({
    q: params.q?.trim() ?? "",
    state: params.state?.trim() ?? "",
    county: params.county?.trim() ?? "",
    city: params.city?.trim() ?? "",
    category: params.category?.trim() ?? "",
    service: params.service?.trim() ?? "",
    tag: params.tag?.trim() ?? "",
    coverage: params.coverage?.trim() ?? "",
    intake: params.intake?.trim() ?? "",
    filter: params.filter?.trim() ?? "",
  });
}

export function buildResourceFiltersFromPageParams(
  params: ResourcesPageSearchParams,
  categoryId?: string
) {
  return {
    query: params.q,
    state: params.state,
    county: params.county,
    city: params.city,
    category: categoryId ?? params.category,
    service: params.service,
    tag: params.tag,
    coverage:
      params.coverage && isValidCoverage(params.coverage)
        ? params.coverage
        : undefined,
    intake: parseIntakeFilterParam(params.intake),
    recentlyAdded: params.filter === "recent",
  };
}
