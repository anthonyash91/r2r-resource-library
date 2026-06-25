import type { Resource, ResourceFilters } from "@/types";
import {
  applySearchQueryFilter,
  resourceMatchesTextQuery,
  type LocationCatalog,
} from "@/lib/resource-search";
import { parseZipFromSearchQuery } from "@/lib/resources-search-params";
import {
  flattenZipPartition,
  partitionResourcesByZip,
  type ZipLocation,
} from "@/lib/resource-zip-search";
import {
  filterResourcesByIntakeSignals,
} from "@/lib/intake-signals";
import {
  isStatewideResource,
  resourceServesCounty,
  resourcesForCountyAttributeScope,
  sortResourcesByCountyRelevance,
} from "@/lib/resource-coverage";
import { normalizeService } from "@/lib/service-types";

function zipKeywordFromFilters(filters: ResourceFilters): string | undefined {
  if (filters.zip?.trim()) return filters.query?.trim() || undefined;
  if (!filters.query?.trim()) return undefined;

  const parsed = parseZipFromSearchQuery(filters.query);
  return parsed?.textQuery?.trim() || undefined;
}

/** Narrow a preloaded pool to match DB-level filters on the resources query. */
export function narrowResourcePool(
  pool: Resource[],
  filters: ResourceFilters,
  zipSearch: ZipLocation | null
): Resource[] {
  let results = pool;
  const scoped: ResourceFilters = { ...filters };

  if (zipSearch && !scoped.state) {
    scoped.state = zipSearch.state;
  }

  if (scoped.state) {
    results = results.filter((resource) => resource.state === scoped.state);
  }
  if (scoped.city) {
    results = results.filter((resource) => resource.city === scoped.city);
  }
  if (scoped.category) {
    results = results.filter((resource) => resource.category_id === scoped.category);
  }
  if (scoped.featured) {
    results = results.filter((resource) => resource.is_featured);
  }
  if (scoped.recentlyAdded) {
    const cutoff = Date.now() - 14 * 86400000;
    results = results.filter(
      (resource) => new Date(resource.created_at).getTime() >= cutoff
    );
  }

  return results;
}

export function filterLoadedResources(
  resources: Resource[],
  filters: ResourceFilters,
  zipSearch: ZipLocation | null,
  locationCatalog?: LocationCatalog | null
): Resource[] {
  let results = resources;

  if (filters.county) {
    results = results.filter((resource) => resourceServesCounty(resource, filters.county!));
    results = sortResourcesByCountyRelevance(results, filters.county);
  }
  if (filters.query?.trim() && !zipSearch && locationCatalog) {
    results = applySearchQueryFilter(results, filters.query, locationCatalog);
  }
  if (filters.service || filters.tag) {
    const attributePool = filters.county
      ? resourcesForCountyAttributeScope(results, filters.county)
      : results;
    results = attributePool;
    if (filters.service) {
      const service = normalizeService(filters.service).toLowerCase();
      results = results.filter((resource) =>
        resource.services.some((svc) => normalizeService(svc).toLowerCase() === service)
      );
    }
    if (filters.tag) {
      const tag = filters.tag.toLowerCase();
      results = results.filter((resource) =>
        resource.tags.some((item) => item.toLowerCase() === tag)
      );
    }
  }
  if (filters.coverage === "statewide") {
    results = results.filter((resource) => isStatewideResource(resource));
  }
  if (filters.coverage === "multi") {
    results = results.filter((resource) => resource.coverage === "multi");
  }
  if (filters.eligibility) {
    const eligibility = filters.eligibility.toLowerCase();
    results = results.filter((resource) =>
      resource.eligibility?.toLowerCase().includes(eligibility)
    );
  }
  if (filters.intake?.length) {
    results = filterResourcesByIntakeSignals(results, filters.intake);
  }

  if (zipSearch) {
    const zipKeyword = zipKeywordFromFilters(filters);
    let zipPool = results.filter(
      (resource) => resource.state === zipSearch.state || isStatewideResource(resource)
    );
    if (zipKeyword) {
      zipPool = zipPool.filter((resource) => resourceMatchesTextQuery(resource, zipKeyword));
    }
    return flattenZipPartition(partitionResourcesByZip(zipPool, zipSearch));
  }

  return results;
}
