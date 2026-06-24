import type {
  Resource,
  Category,
  ResourceFilters,
  Faq,
  Announcement,
  AnalyticsSummary,
  Profile,
  AdminUserListItem,
  CmsPage,
} from "@/types";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import { createClient } from "@/lib/supabase/server";
import { fetchAllRows } from "@/lib/supabase/fetch-all-rows";
import {
  emptyAnalyticsSummary,
} from "@/lib/analytics-empty";
import {
  aggregateRecentActivity,
  recentActivitySinceIso,
} from "@/lib/analytics-recent-activity";
import { MAX_FEATURED_RESOURCES } from "@/lib/featured-resources-storage";
import { isAnnouncementActive } from "@/lib/announcements";
import { getServerLocale } from "@/i18n/server";
import {
  localizeAnnouncements,
  localizeCategories,
  localizeDayLabels,
  localizeFaqs,
  localizeResource,
  localizeResources,
  getLocalizedHomepage,
  resolveSiteBranding,
  type SiteBranding,
} from "@/i18n/localize-content";
import { EDITABLE_SITE_CONTENT_FIELDS } from "@/lib/site-content-fields";
import { getAboutContentAdminValues, resolveAboutPageContent } from "@/lib/about-content";
import { getContactContentAdminValues, resolveContactPageContent } from "@/lib/contact-content";
import {
  getAccessibilityContentAdminValues,
  getLegalDocumentAdminValues,
  resolveAccessibilityPageContent,
  resolveLegalDocumentContent,
} from "@/lib/legal-content";
import { createTranslator } from "@/i18n/translator";
import {
  applySearchQueryFilter,
  type LocationCatalog,
} from "@/lib/resource-search";
import {
  resourceServesCounty,
  sortResourcesByCountyRelevance,
  isStatewideResource,
  resourcesForLocationFacets,
  resourcesForCountyAttributeScope,
  collectResourceServices,
} from "@/lib/resource-coverage";
import { normalizeService, normalizeServices } from "@/lib/service-types";
import { getStateCounties } from "@/lib/states/counties";
import {
  filterResourcesByIntakeSignals,
} from "@/lib/intake-signals";
import {
  buildResourceFilterOptions,
  type ResourceFilterFacetParams,
} from "@/lib/resource-filter-facets";
import { pickRelatedResources } from "@/lib/related-resources";

export async function getCategories(): Promise<Category[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data, error } = await supabase
    .from("categories")
    .select("*")
    .eq("is_active", true)
    .order("sort_order");

  if (error || !data) return [];
  return localizeCategories(data as Category[], locale);
}

async function getLocationCatalog(): Promise<LocationCatalog> {
  const [states, cities, counties] = await Promise.all([
    getStates(),
    getCities(),
    getCounties(),
  ]);
  return { states, cities, counties };
}

type ResourcesQueryClient = NonNullable<Awaited<ReturnType<typeof createClient>>>;

function buildResourcesSelectQuery(client: ResourcesQueryClient, filters: ResourceFilters) {
  let query = client
    .from("resources")
    .select("*, category:categories(*)")
    .eq("status", filters.status ?? "active");

  if (filters.state) query = query.eq("state", filters.state);
  if (filters.city) query = query.eq("city", filters.city);
  if (filters.category) query = query.eq("category_id", filters.category);
  if (filters.featured) query = query.eq("is_featured", true);
  if (filters.recentlyAdded) {
    const cutoff = new Date(Date.now() - 14 * 86400000).toISOString();
    query = query.gte("created_at", cutoff);
  }

  return query.order("name");
}

export async function getResources(filters: ResourceFilters = {}): Promise<Resource[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data, error } = await fetchAllRows<Resource>(async (range) =>
    buildResourcesSelectQuery(supabase, filters).range(range.from, range.to)
  );
  if (error || !data.length) return [];

  let results = localizeResources(data, locale).map((resource) => ({
    ...resource,
    services: normalizeServices(resource.services),
  }));
  if (filters.county) {
    results = results.filter((r) => resourceServesCounty(r, filters.county!));
    results = sortResourcesByCountyRelevance(results, filters.county);
  }
  if (filters.query?.trim()) {
    const catalog = await getLocationCatalog();
    results = applySearchQueryFilter(results, filters.query, catalog);
  }
  if (filters.service || filters.tag) {
    const attributePool = filters.county
      ? resourcesForCountyAttributeScope(results, filters.county)
      : results;
    results = attributePool;
    if (filters.service) {
      const s = normalizeService(filters.service).toLowerCase();
      results = results.filter((resource) =>
        resource.services.some((svc) => normalizeService(svc).toLowerCase() === s)
      );
    }
    if (filters.tag) {
      const tag = filters.tag.toLowerCase();
      results = results.filter((resource) =>
        resource.tags.some((t) => t.toLowerCase() === tag)
      );
    }
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
  return results;
}

export async function getActiveResourceCount(): Promise<number> {
  if (!isSupabaseConfigured()) return 0;

  const supabase = await createClient();
  if (!supabase) return 0;

  const { count, error } = await supabase
    .from("resources")
    .select("id", { count: "exact", head: true })
    .eq("status", "active");

  if (error || count == null) return 0;
  return count;
}

export type { SiteBranding };

async function fetchHomepageContentRaw(): Promise<Record<string, string>> {
  if (!isSupabaseConfigured()) return {};

  const supabase = await createClient();
  if (!supabase) return {};

  const { data } = await supabase.from("homepage_content").select("key, value");
  if (!data) return {};

  return data.reduce(
    (acc, item) => ({ ...acc, [item.key]: item.value }),
    {} as Record<string, string>
  );
}

export async function getSiteBranding(): Promise<SiteBranding> {
  const locale = await getServerLocale();
  const homepage = await fetchHomepageContentRaw();
  return resolveSiteBranding(homepage, locale);
}

export async function getAboutPageContent() {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return resolveAboutPageContent(store, locale);
}

export async function getAboutContentAdmin() {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return getAboutContentAdminValues(store, locale);
}

export async function getContactPageContent() {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return resolveContactPageContent(store, locale);
}

export async function getContactContentAdmin() {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return getContactContentAdminValues(store, locale);
}

export async function getLegalDocumentContent(slug: "privacy" | "terms") {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return resolveLegalDocumentContent(slug, store, locale);
}

export async function getLegalDocumentAdmin(slug: "privacy" | "terms") {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return getLegalDocumentAdminValues(slug, store, locale);
}

export async function getAccessibilityPageContent() {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return resolveAccessibilityPageContent(store, locale);
}

export async function getAccessibilityContentAdmin() {
  const locale = await getServerLocale();
  const store = await fetchHomepageContentRaw();
  return getAccessibilityContentAdminValues(store, locale);
}

export async function getFeaturedResources(limit = MAX_FEATURED_RESOURCES): Promise<Resource[]> {
  const featured = await getResources({ featured: true, status: "active" });
  return featured.slice(0, limit);
}

export async function getHomepageContentAdmin(): Promise<Record<string, string>> {
  const homepage = await fetchHomepageContentRaw();

  return EDITABLE_SITE_CONTENT_FIELDS.reduce(
    (acc, field) => ({ ...acc, [field]: homepage[field] ?? "" }),
    {} as Record<string, string>
  );
}

export async function getAllFaqsAdmin(): Promise<Faq[]> {
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase.from("faqs").select("*").order("sort_order");
  return (data as Faq[]) ?? [];
}

export async function getAllAnnouncementsAdmin(): Promise<Announcement[]> {
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("announcements")
    .select("*")
    .order("is_pinned", { ascending: false })
    .order("created_at", { ascending: false });

  return (data as Announcement[]) ?? [];
}

export async function getResourceById(id: string): Promise<Resource | null> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return null;

  const supabase = await createClient();
  if (!supabase) return null;

  const { data, error } = await supabase
    .from("resources")
    .select("*, category:categories(*)")
    .eq("id", id)
    .single();

  if (error || !data) return null;
  return localizeResource(data as Resource, locale);
}

export async function getRelatedResources(
  resource: Resource,
  limit = 4
): Promise<Resource[]> {
  const filters: ResourceFilters = { category: resource.category_id };
  if (resource.state?.trim()) {
    filters.state = resource.state;
  }

  const candidates = await getResources(filters);
  return pickRelatedResources(resource, candidates, limit);
}

export async function getStates(): Promise<string[]> {
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data, error } = await fetchAllRows<{ state: string | null }>(async (range) =>
    supabase
      .from("resources")
      .select("state")
      .eq("status", "active")
      .not("state", "is", null)
      .order("state")
      .range(range.from, range.to)
  );

  if (error) return [];
  return [...new Set(data.map((r) => r.state).filter(Boolean) as string[])].sort();
}

export async function getCounties(state?: string): Promise<string[]> {
  const canonical = getStateCounties(state);
  if (canonical.length) return [...canonical];

  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data, error } = await fetchAllRows<{ county: string | null }>(async (range) => {
    let pageQuery = supabase
      .from("resources")
      .select("county")
      .eq("status", "active")
      .not("county", "is", null)
      .order("county");
    if (state) pageQuery = pageQuery.eq("state", state);
    return pageQuery.range(range.from, range.to);
  });
  if (error) return [];
  const fromResources = new Set<string>();
  for (const row of data) {
    if (row.county) fromResources.add(row.county as string);
  }
  return [...fromResources].sort((a, b) => a.localeCompare(b));
}

export async function getCities(state?: string, county?: string): Promise<string[]> {
  const resources = await getResources({ state, status: "active" });
  const scoped = resourcesForLocationFacets(resources, county);
  return [
    ...new Set(scoped.map((resource) => resource.city).filter(Boolean) as string[]),
  ].sort((a, b) => a.localeCompare(b));
}

export async function getCategoriesForLocation(
  state?: string,
  county?: string
): Promise<Category[]> {
  const resources = await getResources({
    state,
    status: "active",
  });
  const scoped = resourcesForLocationFacets(resources, county);
  if (scoped.length === 0) return [];

  const categoryIds = new Set(scoped.map((resource) => resource.category_id));
  const categories = await getCategories();
  return categories.filter((category) => categoryIds.has(category.id));
}

export async function getResourceFilterOptions(params: ResourceFilterFacetParams = {}) {
  const { state, county, city, categorySlug, service, intake } = params;
  const resources = await getResources({ state, status: "active" });

  const allCategories = await getCategories();
  let categoryId = params.categoryId;
  if (!categoryId && categorySlug) {
    categoryId = allCategories.find((category) => category.slug === categorySlug)?.id;
  }

  const resolvedParams: ResourceFilterFacetParams = {
    state,
    county,
    city,
    categorySlug,
    categoryId,
    service,
    intake,
  };

  const stateCounties = state ? [...getStateCounties(state)] : [];
  return buildResourceFilterOptions(resources, allCategories, resolvedParams, stateCounties);
}

export async function getServices(state?: string, county?: string): Promise<string[]> {
  const resources = await getResources({ state, status: "active" });
  return collectResourceServices(resourcesForLocationFacets(resources, county));
}

export async function getFaqs(): Promise<Faq[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("faqs")
    .select("*")
    .eq("is_active", true)
    .order("sort_order");

  return localizeFaqs((data as Faq[]) ?? [], locale);
}

export async function getAnnouncements(): Promise<Announcement[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("announcements")
    .select("*")
    .eq("status", "published")
    .order("is_pinned", { ascending: false })
    .order("created_at", { ascending: false });

  const active = ((data as Announcement[]) ?? []).filter((announcement) =>
    isAnnouncementActive(announcement)
  );
  return localizeAnnouncements(active, locale);
}

export async function getHomepageContent(): Promise<Record<string, string>> {
  const locale = await getServerLocale();
  const homepage = await fetchHomepageContentRaw();
  return getLocalizedHomepage(homepage, locale);
}

export async function getAnalytics(): Promise<AnalyticsSummary> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) {
    const analytics = emptyAnalyticsSummary();
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
    const analytics = emptyAnalyticsSummary();
    return {
      ...analytics,
      recentActivity: analytics.recentActivity.map((item) => ({
        ...item,
        date: localizeDayLabels([item.date], locale)[0] ?? item.date,
      })),
    };
  }

  const [
    totalResourcesRes,
    activeResourcesRes,
    featuredResourcesRes,
    categoriesRes,
    savesRes,
    mostViewedRes,
    mostSavedRes,
    recentViewsRes,
    recentSavesRes,
    activeResourcesPaged,
    viewCountsPaged,
  ] = await Promise.all([
    supabase.from("resources").select("id", { count: "exact", head: true }),
    supabase.from("resources").select("id", { count: "exact", head: true }).eq("status", "active"),
    supabase
      .from("resources")
      .select("id", { count: "exact", head: true })
      .eq("status", "active")
      .eq("is_featured", true),
    supabase.from("categories").select("id", { count: "exact", head: true }).eq("is_active", true),
    supabase.from("saved_resources").select("id", { count: "exact", head: true }),
    supabase
      .from("resources")
      .select("*")
      .gt("view_count", 0)
      .order("view_count", { ascending: false })
      .limit(5),
    supabase
      .from("resources")
      .select("*")
      .gt("save_count", 0)
      .order("save_count", { ascending: false })
      .limit(5),
    supabase
      .from("resource_views")
      .select("viewed_at")
      .gte("viewed_at", recentActivitySinceIso()),
    supabase
      .from("saved_resources")
      .select("created_at")
      .gte("created_at", recentActivitySinceIso()),
    fetchAllRows<Resource & { category?: { name: string } }>(async (range) =>
      supabase
        .from("resources")
        .select("*, category:categories(name)")
        .eq("status", "active")
        .order("name")
        .range(range.from, range.to)
    ),
    fetchAllRows<{ view_count: number | null }>(async (range) =>
      supabase
        .from("resources")
        .select("view_count")
        .order("id")
        .range(range.from, range.to)
    ),
  ]);

  const resources = activeResourcesPaged.data;
  const stateMap = new Map<string, number>();
  const catMap = new Map<string, number>();

  for (const r of resources) {
    if (r.state) stateMap.set(r.state, (stateMap.get(r.state) ?? 0) + 1);
    const catName = r.category?.name;
    if (catName) catMap.set(catName, (catMap.get(catName) ?? 0) + 1);
  }

  const totalViews = viewCountsPaged.data.reduce(
    (sum, row) => sum + (row.view_count ?? 0),
    0
  );

  const recentActivityRaw = aggregateRecentActivity(
    (recentViewsRes.data ?? []) as { viewed_at: string }[],
    (recentSavesRes.data ?? []) as { created_at: string }[]
  );

  return {
    totalResources: totalResourcesRes.count ?? 0,
    activeResources: activeResourcesRes.count ?? 0,
    featuredResources: featuredResourcesRes.count ?? 0,
    totalCategories: categoriesRes.count ?? 0,
    totalViews,
    totalSaves: savesRes.count ?? 0,
    resourcesByState: Array.from(stateMap.entries())
      .map(([state, count]) => ({ state, count }))
      .sort((a, b) => b.count - a.count),
    resourcesByCategory: Array.from(catMap.entries())
      .map(([category, count]) => ({ category, count }))
      .sort((a, b) => b.count - a.count),
    mostViewed: (mostViewedRes.data ?? []) as Resource[],
    mostSaved: (mostSavedRes.data ?? []) as Resource[],
    recentActivity: recentActivityRaw.map((item) => ({
      ...item,
      date: localizeDayLabels([item.date], locale)[0] ?? item.date,
    })),
  };
}

type SavedResourceRow = {
  resource_id: string;
  resource: Resource | null;
};

export async function getSavedResourcesForUser(
  userId: string,
  locale: Awaited<ReturnType<typeof getServerLocale>>
): Promise<Resource[]> {
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("saved_resources")
    .select("resource_id, resource:resources(*, category:categories(*))")
    .eq("user_id", userId)
    .order("created_at", { ascending: false });

  if (!data) return [];

  const rows = data as unknown as SavedResourceRow[];
  const resources = rows
    .map((row) => row.resource)
    .filter((resource): resource is Resource => resource != null);

  return localizeResources(resources, locale);
}

export async function getAllResourcesAdmin(): Promise<Resource[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data, error } = await fetchAllRows<Resource>(async (range) =>
    supabase
      .from("resources")
      .select("*, category:categories(*)")
      .order("updated_at", { ascending: false })
      .range(range.from, range.to)
  );

  if (error) return [];
  return localizeResources(data, locale);
}

export async function getAllCategoriesAdmin(): Promise<Category[]> {
  const locale = await getServerLocale();
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("categories")
    .select("*")
    .order("sort_order");

  return localizeCategories((data as Category[]) ?? [], locale);
}

export async function getAllUsersAdmin(): Promise<AdminUserListItem[]> {
  if (!isSupabaseConfigured()) return [];

  const supabase = await createClient();
  if (!supabase) return [];

  const { data } = await supabase
    .from("profiles")
    .select("*, facility:facilities(name)")
    .order("created_at", { ascending: false });

  return ((data ?? []) as Array<Profile & { facility?: { name: string } | null }>).map(
    (row) => {
      const { facility, ...profile } = row;
      return {
        ...(profile as Profile),
        facility_name: facility?.name ?? null,
      };
    }
  );
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
        meta_description: t("about.description"),
        status: "published",
        sort_order: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        published_at: new Date().toISOString(),
      },
      {
        id: "page-contact",
        title: t("contact.defaultTitle"),
        slug: "contact",
        content: t("contact.defaultContent"),
        meta_description: t("contact.description"),
        status: "published",
        sort_order: 2,
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
  const locale = await getServerLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    const pages = await getCmsPages();
    return pages.find((page) => page.slug === slug && page.status === "published") ?? null;
  }

  const supabase = await createClient();
  if (!supabase) {
    if (slug === "about") {
      return {
        id: "page-about",
        title: t("about.defaultTitle"),
        slug: "about",
        content: t("about.defaultContent"),
        meta_description: t("about.description"),
        status: "published",
        sort_order: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        published_at: new Date().toISOString(),
      };
    }
    if (slug === "contact") {
      return {
        id: "page-contact",
        title: t("contact.defaultTitle"),
        slug: "contact",
        content: t("contact.defaultContent"),
        meta_description: t("contact.description"),
        status: "published",
        sort_order: 2,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        published_at: new Date().toISOString(),
      };
    }
    return null;
  }

  const { data } = await supabase
    .from("cms_pages")
    .select("*")
    .eq("slug", slug)
    .eq("status", "published")
    .maybeSingle();

  return (data as CmsPage | null) ?? null;
}

export async function getCategoryBySlug(slug: string): Promise<Category | null> {
  const categories = await getCategories();
  return categories.find((c) => c.slug === slug) ?? null;
}
