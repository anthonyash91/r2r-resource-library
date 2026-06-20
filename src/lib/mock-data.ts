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

export { MOCK_CATEGORIES };

const now = new Date().toISOString();

/** Kentucky reentry resources researched and verified for Reentry to Recovery */
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

  if (filters.query) {
    const q = filters.query.toLowerCase();
    results = results.filter(
      (r) =>
        r.name.toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        r.services.some((s) => s.toLowerCase().includes(q)) ||
        r.tags.some((t) => t.toLowerCase().includes(q)) ||
        (r.eligibility?.toLowerCase().includes(q) ?? false)
    );
  }
  if (filters.state) results = results.filter((r) => r.state === filters.state);
  if (filters.county) results = results.filter((r) => r.county === filters.county);
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
  if (filters.eligibility) {
    const e = filters.eligibility.toLowerCase();
    results = results.filter((r) => r.eligibility?.toLowerCase().includes(e));
  }
  if (filters.recentlyAdded) {
    const cutoff = new Date(Date.now() - 14 * 86400000);
    results = results.filter((r) => new Date(r.created_at) >= cutoff);
  }
  if (filters.featured) {
    results = results.filter((r) => r.is_featured);
  }

  return results;
}

export function getMockAnalytics(): AnalyticsSummary {
  return {
    totalResources: 0,
    totalUsers: 0,
    totalSaves: 0,
    resourcesByState: [],
    resourcesByCategory: [],
    mostViewed: [],
    mostSaved: [],
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
  const resources = state ? MOCK_RESOURCES.filter((r) => r.state === state) : MOCK_RESOURCES;
  return [...new Set(resources.map((r) => r.county).filter(Boolean) as string[])].sort();
}

export function getMockCities(state?: string, county?: string): string[] {
  let resources = MOCK_RESOURCES;
  if (state) resources = resources.filter((r) => r.state === state);
  if (county) resources = resources.filter((r) => r.county === county);
  return [...new Set(resources.map((r) => r.city).filter(Boolean) as string[])].sort();
}

export function getMockServices(): string[] {
  const services = new Set<string>();
  MOCK_RESOURCES.forEach((r) => r.services.forEach((s) => services.add(s)));
  return [...services].sort();
}
