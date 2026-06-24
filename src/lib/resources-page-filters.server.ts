import { getCategoryBySlug } from "@/lib/data";
import {
  buildResourceFiltersFromPageParams,
  type ResourcesPageSearchParams,
} from "@/lib/resources-page-filters";
import type { ResourceFilters } from "@/types";

export async function resolveResourcesPageFilters(
  params: ResourcesPageSearchParams
): Promise<ResourceFilters> {
  let categoryId = params.category;
  if (params.category) {
    const cat = await getCategoryBySlug(params.category);
    if (cat) categoryId = cat.id;
  }

  return buildResourceFiltersFromPageParams(params, categoryId);
}
