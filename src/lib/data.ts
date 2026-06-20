import type {
  Resource,
  Category,
  ResourceFilters,
  Faq,
  Announcement,
  AnalyticsSummary,
  Profile,
  CmsPage,
} from "@/types";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import { createClient } from "@/lib/supabase/server";
import {
  MOCK_RESOURCES,
  MOCK_CATEGORIES,
  MOCK_FAQS,
  MOCK_ANNOUNCEMENTS,
  MOCK_HOMEPAGE,
  filterMockResources,
  getMockAnalytics,
  getMockStates,
  getMockCounties,
  getMockCities,
  getMockServices,
} from "@/lib/mock-data";
import { MAX_FEATURED_RESOURCES } from "@/lib/featured-resources-storage";
import { getServerLocale } from "@/i18n/server";
import {
  localizeAnnouncements,
  localizeCategories,
  localizeDayLabels,
  localizeFaqs,
  localizeResource,
  localizeResources,
  getLocalizedHomepage,
} from "@/i18n/localize-content";
import { createTranslator } from "@/i18n/translator";

export async function getCategories(): Promise<Category[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) {
    return localizeCategories(MOCK_CATEGORIES.filter((c) => c.is_active), locale);
  }

  const supabase = await createClient();
  if (!supabase) return MOCK_CATEGORIES.filter((c) => c.is_active);

  const { data, error } = await supabase
    .from("categories")
    .select("*")
    .eq("is_active", true)
    .order("sort_order");

  if (error || !data) return localizeCategories(MOCK_CATEGORIES.filter((c) => c.is_active), locale);
  return localizeCategories(data as Category[], locale);
}

export async function getResources(filters: ResourceFilters = {}): Promise<Resource[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return localizeResources(filterMockResources(filters), locale);

  const supabase = await createClient();
  if (!supabase) return localizeResources(filterMockResources(filters), locale);

  let query = supabase
    .from("resources")
    .select("*, category:categories(*)")
    .eq("status", filters.status ?? "active");

  if (filters.state) query = query.eq("state", filters.state);
  if (filters.county) query = query.eq("county", filters.county);
  if (filters.city) query = query.eq("city", filters.city);
  if (filters.category) query = query.eq("category_id", filters.category);
  if (filters.featured) query = query.eq("is_featured", true);
  if (filters.recentlyAdded) {
    const cutoff = new Date(Date.now() - 14 * 86400000).toISOString();
    query = query.gte("created_at", cutoff);
  }
  if (filters.query) {
    query = query.or(
      `name.ilike.%${filters.query}%,description.ilike.%${filters.query}%`
    );
  }

  query = query.order("name");

  const { data, error } = await query;
  if (error || !data) return localizeResources(filterMockResources(filters), locale);

  let results = localizeResources(data as Resource[], locale);
  if (filters.service) {
    const s = filters.service.toLowerCase();
    results = results.filter((r) =>
      r.services.some((svc) => svc.toLowerCase().includes(s))
    );
  }
  if (filters.tag) {
    const tag = filters.tag.toLowerCase();
    results = results.filter((r) => r.tags.some((t) => t.toLowerCase() === tag));
  }
  if (filters.eligibility) {
    const e = filters.eligibility.toLowerCase();
    results = results.filter((r) => r.eligibility?.toLowerCase().includes(e));
  }
  return results;
}

export async function getFeaturedResources(limit = MAX_FEATURED_RESOURCES): Promise<Resource[]> {
  const featured = await getResources({ featured: true, status: "active" });
  return featured.slice(0, limit);
}

export async function getResourceById(id: string): Promise<Resource | null> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) {
    const resource = MOCK_RESOURCES.find((r) => r.id === id) ?? null;
    return resource ? localizeResource(resource, locale) : null;
  }

  const supabase = await createClient();
  if (!supabase) {
    const resource = MOCK_RESOURCES.find((r) => r.id === id) ?? null;
    return resource ? localizeResource(resource, locale) : null;
  }

  const { data, error } = await supabase
    .from("resources")
    .select("*, category:categories(*)")
    .eq("id", id)
    .single();

  if (error || !data) {
    const resource = MOCK_RESOURCES.find((r) => r.id === id) ?? null;
    return resource ? localizeResource(resource, locale) : null;
  }
  return localizeResource(data as Resource, locale);
}

export async function getRelatedResources(
  resource: Resource,
  limit = 4
): Promise<Resource[]> {
  const all = await getResources({
    category: resource.category_id,
  });
  return all.filter((r) => r.id !== resource.id).slice(0, limit);
}

export async function getStates(): Promise<string[]> {
  if (!isSupabaseConfigured()) return getMockStates();

  const supabase = await createClient();
  if (!supabase) return getMockStates();

  const { data } = await supabase
    .from("resources")
    .select("state")
    .eq("status", "active")
    .not("state", "is", null);

  if (!data) return getMockStates();
  return [...new Set(data.map((r) => r.state).filter(Boolean) as string[])].sort();
}

export async function getCounties(state?: string): Promise<string[]> {
  if (!isSupabaseConfigured()) return getMockCounties(state);

  const supabase = await createClient();
  if (!supabase) return getMockCounties(state);

  let query = supabase
    .from("resources")
    .select("county")
    .eq("status", "active")
    .not("county", "is", null);
  if (state) query = query.eq("state", state);

  const { data } = await query;
  if (!data) return getMockCounties(state);
  return [...new Set(data.map((r) => r.county).filter(Boolean) as string[])].sort();
}

export async function getCities(state?: string, county?: string): Promise<string[]> {
  if (!isSupabaseConfigured()) return getMockCities(state, county);

  const supabase = await createClient();
  if (!supabase) return getMockCities(state, county);

  let query = supabase
    .from("resources")
    .select("city")
    .eq("status", "active")
    .not("city", "is", null);
  if (state) query = query.eq("state", state);
  if (county) query = query.eq("county", county);

  const { data } = await query;
  if (!data) return getMockCities(state, county);
  return [...new Set(data.map((r) => r.city).filter(Boolean) as string[])].sort();
}

export async function getServices(): Promise<string[]> {
  if (!isSupabaseConfigured()) return getMockServices();

  const supabase = await createClient();
  if (!supabase) return getMockServices();

  const { data } = await supabase
    .from("resources")
    .select("services")
    .eq("status", "active");

  if (!data) return getMockServices();
  const services = new Set<string>();
  data.forEach((r) => (r.services as string[]).forEach((s) => services.add(s)));
  return [...services].sort();
}

export async function getFaqs(): Promise<Faq[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return localizeFaqs(MOCK_FAQS, locale);

  const supabase = await createClient();
  if (!supabase) return localizeFaqs(MOCK_FAQS, locale);

  const { data } = await supabase
    .from("faqs")
    .select("*")
    .eq("is_active", true)
    .order("sort_order");

  return localizeFaqs((data as Faq[]) ?? MOCK_FAQS, locale);
}

export async function getAnnouncements(): Promise<Announcement[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return localizeAnnouncements(MOCK_ANNOUNCEMENTS, locale);

  const supabase = await createClient();
  if (!supabase) return localizeAnnouncements(MOCK_ANNOUNCEMENTS, locale);

  const { data } = await supabase
    .from("announcements")
    .select("*")
    .eq("status", "published")
    .order("is_pinned", { ascending: false })
    .order("created_at", { ascending: false });

  return localizeAnnouncements((data as Announcement[]) ?? MOCK_ANNOUNCEMENTS, locale);
}

export async function getHomepageContent(): Promise<Record<string, string>> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return getLocalizedHomepage(MOCK_HOMEPAGE, locale);

  const supabase = await createClient();
  if (!supabase) return getLocalizedHomepage(MOCK_HOMEPAGE, locale);

  const { data } = await supabase.from("homepage_content").select("key, value");
  if (!data) return getLocalizedHomepage(MOCK_HOMEPAGE, locale);

  const homepage = data.reduce(
    (acc, item) => ({ ...acc, [item.key]: item.value }),
    {} as Record<string, string>
  );
  return getLocalizedHomepage(homepage, locale);
}

export async function getAnalytics(): Promise<AnalyticsSummary> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) {
    const analytics = getMockAnalytics();
    return {
      ...analytics,
      recentActivity: analytics.recentActivity.map((item) => ({
        ...item,
        date: localizeDayLabels([item.date], locale)[0] ?? item.date,
      })),
    };
  }

  const supabase = await createClient();
  if (!supabase) {
    const analytics = getMockAnalytics();
    return {
      ...analytics,
      recentActivity: analytics.recentActivity.map((item) => ({
        ...item,
        date: localizeDayLabels([item.date], locale)[0] ?? item.date,
      })),
    };
  }

  const [resourcesRes, usersRes, savesRes] = await Promise.all([
    supabase.from("resources").select("*, category:categories(name)").eq("status", "active"),
    supabase.from("profiles").select("id", { count: "exact", head: true }),
    supabase.from("saved_resources").select("id", { count: "exact", head: true }),
  ]);

  const resources = (resourcesRes.data ?? []) as Resource[];
  const stateMap = new Map<string, number>();
  const catMap = new Map<string, number>();

  for (const r of resources) {
    if (r.state) stateMap.set(r.state, (stateMap.get(r.state) ?? 0) + 1);
    const catName = (r as Resource & { category?: { name: string } }).category?.name;
    if (catName) catMap.set(catName, (catMap.get(catName) ?? 0) + 1);
  }

  return {
    totalResources: resources.length,
    totalUsers: usersRes.count ?? 0,
    totalSaves: savesRes.count ?? 0,
    resourcesByState: Array.from(stateMap.entries())
      .map(([state, count]) => ({ state, count }))
      .sort((a, b) => b.count - a.count),
    resourcesByCategory: Array.from(catMap.entries())
      .map(([category, count]) => ({ category, count }))
      .sort((a, b) => b.count - a.count),
    mostViewed: [...resources].sort((a, b) => b.view_count - a.view_count).slice(0, 5),
    mostSaved: [...resources].sort((a, b) => b.save_count - a.save_count).slice(0, 5),
    recentActivity: getMockAnalytics().recentActivity,
  };
}

export async function getAllResourcesAdmin(): Promise<Resource[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return localizeResources(MOCK_RESOURCES, locale);

  const supabase = await createClient();
  if (!supabase) return localizeResources(MOCK_RESOURCES, locale);

  const { data } = await supabase
    .from("resources")
    .select("*, category:categories(*)")
    .order("updated_at", { ascending: false });

  return localizeResources((data as Resource[]) ?? MOCK_RESOURCES, locale);
}

export async function getAllCategoriesAdmin(): Promise<Category[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return localizeCategories(MOCK_CATEGORIES, locale);

  const supabase = await createClient();
  if (!supabase) return localizeCategories(MOCK_CATEGORIES, locale);

  const { data } = await supabase
    .from("categories")
    .select("*")
    .order("sort_order");

  return localizeCategories((data as Category[]) ?? MOCK_CATEGORIES, locale);
}

export async function getAllUsersAdmin(): Promise<Profile[]> {
  if (!isSupabaseConfigured()) {
    return [
      {
        id: "user-1",
        email: "user@example.com",
        full_name: "John Smith",
        role: "user",
        is_active: true,
        phone: null,
        state: "California",
        county: null,
        city: "Los Angeles",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];
  }

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("profiles")
    .select("*")
    .order("created_at", { ascending: false });

  return (data as Profile[]) ?? [];
}

export async function getCmsPages(): Promise<CmsPage[]> {
  const locale = await getServerLocale();
  const { t } = createTranslator(locale);
  if (!isSupabaseConfigured()) {
    return [
      {
        id: "page-about",
        title: t("about.defaultTitle"),
        slug: "about",
        content: t("about.defaultContent"),
        meta_description: t("mock.aboutMeta"),
        status: "published",
        sort_order: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        published_at: new Date().toISOString(),
      },
    ];
  }

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("cms_pages")
    .select("*")
    .order("sort_order");

  return (data as CmsPage[]) ?? [];
}

export async function getCmsPageBySlug(slug: string): Promise<CmsPage | null> {
  const pages = await getCmsPages();
  return pages.find((p) => p.slug === slug && p.status === "published") ?? null;
}

export async function getCategoryBySlug(slug: string): Promise<Category | null> {
  const categories = await getCategories();
  return categories.find((c) => c.slug === slug) ?? null;
}
