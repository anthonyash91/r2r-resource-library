import type {
  Resource,
  CmsPage,
  Faq,
  Announcement,
  Profile,
  AnalyticsSummary,
  ResourceFilters,
} from "@/types";
import { MOCK_CATEGORIES } from "./mock-data-categories";
import { generateMockResources } from "./generate-mock-resources";

export { MOCK_CATEGORIES };

const now = new Date().toISOString();
const weekAgo = new Date(Date.now() - 7 * 86400000).toISOString();

export const MOCK_RESOURCES: Resource[] = generateMockResources(MOCK_CATEGORIES);

export const MOCK_FAQS: Faq[] = [
  { id: "faq-1", question: "Who can use this resource library?", answer: "Anyone can search and view resources. Creating an account lets you save resources and track your personal list.", category: "General", sort_order: 1, is_active: true, created_at: now, updated_at: now },
  { id: "faq-2", question: "Is this service free?", answer: "Yes. Searching resources and creating an account are completely free. Individual programs may have their own eligibility requirements.", category: "General", sort_order: 2, is_active: true, created_at: now, updated_at: now },
  { id: "faq-3", question: "How do I save a resource?", answer: "Click the 'Save' button on any resource card or detail page. You must be signed in. View all saved resources from your dashboard or the Saved page.", category: "Using the Site", sort_order: 3, is_active: true, created_at: now, updated_at: now },
  { id: "faq-4", question: "How often is information updated?", answer: "We review resources regularly. Each listing shows a 'Last Updated' date. If you find outdated information, please contact us.", category: "Using the Site", sort_order: 4, is_active: true, created_at: now, updated_at: now },
  { id: "faq-5", question: "Can I suggest a new resource?", answer: "Yes! Contact us through the About page or ask your case manager to submit a resource for review.", category: "General", sort_order: 5, is_active: true, created_at: now, updated_at: now },
];

export const MOCK_ANNOUNCEMENTS: Announcement[] = [
  { id: "ann-1", title: "100+ Resources Now Available", content: "We expanded our library to over 100 programs across all 50 states. Browse housing, employment, healthcare, and more near you.", status: "published", is_pinned: true, starts_at: weekAgo, ends_at: null, created_at: weekAgo, updated_at: now },
];

export const MOCK_HOMEPAGE = {
  hero_headline: "Find the Resources You Need for a Successful Reentry",
  hero_subheadline: "Search local, state, and national programs that can help with housing, employment, healthcare, recovery, transportation, education, and more.",
};

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
  const stateMap = new Map<string, number>();
  const catMap = new Map<string, number>();
  for (const r of MOCK_RESOURCES) {
    if (r.state) stateMap.set(r.state, (stateMap.get(r.state) ?? 0) + 1);
    if (r.category) catMap.set(r.category.name, (catMap.get(r.category.name) ?? 0) + 1);
  }
  return {
    totalResources: MOCK_RESOURCES.length,
    totalUsers: 248,
    totalSaves: MOCK_RESOURCES.reduce((s, r) => s + r.save_count, 0),
    resourcesByState: Array.from(stateMap.entries()).map(([state, count]) => ({ state, count })).sort((a, b) => b.count - a.count),
    resourcesByCategory: Array.from(catMap.entries()).map(([category, count]) => ({ category, count })).sort((a, b) => b.count - a.count),
    mostViewed: [...MOCK_RESOURCES].sort((a, b) => b.view_count - a.view_count).slice(0, 5),
    mostSaved: [...MOCK_RESOURCES].sort((a, b) => b.save_count - a.save_count).slice(0, 5),
    recentActivity: [
      { date: "Mon", views: 45, saves: 12 },
      { date: "Tue", views: 52, saves: 18 },
      { date: "Wed", views: 38, saves: 9 },
      { date: "Thu", views: 61, saves: 22 },
      { date: "Fri", views: 55, saves: 15 },
      { date: "Sat", views: 28, saves: 7 },
      { date: "Sun", views: 22, saves: 5 },
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
