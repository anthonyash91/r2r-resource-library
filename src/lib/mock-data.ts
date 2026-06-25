import type {
  Resource,
  Faq,
  Announcement,
  Profile,
  AnalyticsSummary,
  ResourceFilters,
} from "@/types";
import { MOCK_CATEGORIES } from "./mock-data-categories";
import { KENTUCKY_RESOURCES } from "./kentucky/resources";
import {
  applySearchQueryFilter,
  buildLocationCatalog,
  resourceMatchesTextQuery,
} from "./resource-search";
import { parseZipFromSearchQuery } from "./resources-search-params";
import { lookupZip } from "./zip-lookup";
import {
  flattenZipPartition,
  partitionResourcesByZip,
} from "./resource-zip-search";
import {
  resourceServesCounty,
  sortResourcesByCountyRelevance,
  isStatewideResource,
} from "./resource-coverage";
import { getStateCounties } from "./states/counties";
import { filterResourcesByIntakeSignals } from "@/lib/intake-signals";

export { MOCK_CATEGORIES };

const now = new Date().toISOString();

/** @deprecated Demo mode removed — resources load from Supabase only. */
export const MOCK_RESOURCES: Resource[] = KENTUCKY_RESOURCES;

export const MOCK_FAQS: Faq[] = [];

export const MOCK_ANNOUNCEMENTS: Announcement[] = [];

export const MOCK_HOMEPAGE: Record<string, string> = {};

export const MOCK_ADMIN_USER: Profile = {
  id: "admin-demo",
  email: "admin@reentrylibrary.org",
  full_name: "Demo Admin",
  role: "admin",
  is_active: true,
  phone: null,
  state: null,
  county: null,
  city: null,
  created_at: now,
  updated_at: now,
};

export function filterMockResources(filters: ResourceFilters): Resource[] {
  let results = MOCK_RESOURCES.filter((r) => r.status === (filters.status ?? "active"));
  const catalog = buildLocationCatalog(MOCK_RESOURCES);
  const zipSearch =
    (filters.zip?.trim() ? lookupZip(filters.zip) : null) ??
    (filters.query?.trim()
      ? (() => {
          const parsed = parseZipFromSearchQuery(filters.query);
          return parsed ? lookupZip(parsed.zip) : null;
        })()
      : null);

  if (filters.state) results = results.filter((r) => r.state === filters.state);
  if (filters.county) {
    results = results.filter((r) => resourceServesCounty(r, filters.county!));
    results = sortResourcesByCountyRelevance(results, filters.county);
  }
  if (filters.city) results = results.filter((r) => r.city === filters.city);
  if (filters.category) {
    results = results.filter(
      (r) => r.category?.slug === filters.category || r.category_id === filters.category
    );
  }
  if (filters.service) {
    const s = filters.service.toLowerCase();
    results = results.filter((r) => r.services.some((svc) => svc.toLowerCase().includes(s)));
  }
  if (filters.tag) {
    const tag = filters.tag.toLowerCase();
    results = results.filter((r) => r.tags.some((t) => t.toLowerCase() === tag));
  }
  if (filters.coverage === "statewide") {
    results = results.filter((r) => isStatewideResource(r));
  }
  if (filters.coverage === "multi") {
    results = results.filter((r) => r.coverage === "multi");
  }
  if (filters.eligibility) {
    const e = filters.eligibility.toLowerCase();
    results = results.filter((r) => r.eligibility?.toLowerCase().includes(e));
  }
  if (filters.intake?.length) {
    results = filterResourcesByIntakeSignals(results, filters.intake);
  }
  if (filters.recentlyAdded) {
    const cutoff = new Date(Date.now() - 14 * 86400000);
    results = results.filter((r) => new Date(r.created_at) >= cutoff);
  }
  if (filters.featured) {
    results = results.filter((r) => r.is_featured);
  }
  if (filters.query && !zipSearch) {
    results = applySearchQueryFilter(results, filters.query, catalog);
  }

  if (zipSearch) {
    const zipKeyword = filters.zip?.trim()
      ? filters.query?.trim() || undefined
      : parseZipFromSearchQuery(filters.query ?? "")?.textQuery?.trim();
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

export function getMockAnalytics(): AnalyticsSummary {
  const activeResources = MOCK_RESOURCES.filter((r) => r.status === "active");

  return {
    totalResources: MOCK_RESOURCES.length,
    activeResources: activeResources.length,
    featuredResources: activeResources.filter((r) => r.is_featured).length,
    totalCategories: MOCK_CATEGORIES.filter((c) => c.is_active).length,
    totalViews: MOCK_RESOURCES.reduce((sum, resource) => sum + resource.view_count, 0),
    totalSaves: 0,
    resourcesByState: [],
    resourcesByCategory: [],
    mostViewed: [...activeResources]
      .filter((r) => r.view_count > 0)
      .sort((a, b) => b.view_count - a.view_count)
      .slice(0, 5),
    mostSaved: [...activeResources]
      .filter((r) => r.save_count > 0)
      .sort((a, b) => b.save_count - a.save_count)
      .slice(0, 5),
    recentActivity: [
      { date: "Mon", views: 0, saves: 0 },
      { date: "Tue", views: 0, saves: 0 },
      { date: "Wed", views: 0, saves: 0 },
      { date: "Thu", views: 0, saves: 0 },
      { date: "Fri", views: 0, saves: 0 },
      { date: "Sat", views: 0, saves: 0 },
      { date: "Sun", views: 0, saves: 0 },
    ],
  };
}

export function getMockStates(): string[] {
  return [...new Set(MOCK_RESOURCES.map((r) => r.state).filter(Boolean) as string[])].sort();
}

export function getMockCounties(state?: string): string[] {
  const canonical = getStateCounties(state);
  if (canonical.length) return [...canonical];
  const resources = MOCK_RESOURCES.filter((r) => r.state === state);
  return [...new Set(resources.map((r) => r.county).filter(Boolean) as string[])].sort();
}

export function getMockCities(state?: string, county?: string): string[] {
  let resources = MOCK_RESOURCES;
  if (state) resources = resources.filter((r) => r.state === state);
  if (county) {
    resources = resources.filter((r) => resourceServesCounty(r, county));
  }
  return [...new Set(resources.map((r) => r.city).filter(Boolean) as string[])].sort();
}

export function getMockServices(): string[] {
  const services = new Set<string>();
  MOCK_RESOURCES.forEach((r) => r.services.forEach((s) => services.add(s)));
  return [...services].sort();
}
