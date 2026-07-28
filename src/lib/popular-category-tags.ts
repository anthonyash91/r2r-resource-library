import type { Category, Resource } from "@/types";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import { createClient } from "@/lib/supabase/server";
import { createAdminClient, isAdminClientConfigured } from "@/lib/supabase/admin";
import { fetchAllRows } from "@/lib/supabase/fetch-all-rows";

export const DEFAULT_POPULAR_CATEGORY_SLUGS = [
  "housing",
  "identification-documents",
  "employment",
  "substance-abuse-recovery",
] as const;

export const POPULAR_TAGS_LIMIT = 4;
export const POPULAR_TAGS_LOOKBACK_DAYS = 90;

export type PopularTag = { label: string; slug: string };

type TranslateFn = (key: string) => string;

type ResourceViewRow = {
  resource: {
    category: { slug: string } | null;
  } | null;
};

type ResourceViewCountRow = {
  view_count: number;
  category: { slug: string } | null;
};

function topSlugsFromCounts(
  counts: Map<string, number>,
  limit = POPULAR_TAGS_LIMIT
): string[] {
  return [...counts.entries()]
    .filter(([, count]) => count > 0)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([slug]) => slug);
}

export function aggregatePopularCategorySlugsFromViewCounts(
  resources: Resource[],
  limit = POPULAR_TAGS_LIMIT
): string[] {
  const counts = new Map<string, number>();

  for (const resource of resources) {
    const slug = resource.category?.slug;
    if (!slug) continue;
    counts.set(slug, (counts.get(slug) ?? 0) + (resource.view_count ?? 0));
  }

  return topSlugsFromCounts(counts, limit);
}

export function resolvePopularTagLabel(t: TranslateFn, slug: string): string {
  if (slug === "housing") return t("home.popularHousingTonight");
  if (slug === "identification-documents") return t("home.popularGetId");
  if (slug === "employment") return t("home.popularFindWork");
  return t(`categories.${slug}.shortName`);
}

export function buildPopularTags(
  categories: Category[],
  slugs: string[],
  t: TranslateFn
): PopularTag[] {
  const activeSlugs = new Set(categories.map((category) => category.slug));
  const seen = new Set<string>();
  const tags: PopularTag[] = [];

  for (const slug of slugs) {
    if (!activeSlugs.has(slug) || seen.has(slug)) continue;
    seen.add(slug);
    tags.push({ slug, label: resolvePopularTagLabel(t, slug) });
    if (tags.length >= POPULAR_TAGS_LIMIT) break;
  }

  if (tags.length >= POPULAR_TAGS_LIMIT) return tags;

  for (const slug of DEFAULT_POPULAR_CATEGORY_SLUGS) {
    if (!activeSlugs.has(slug) || seen.has(slug)) continue;
    seen.add(slug);
    tags.push({ slug, label: resolvePopularTagLabel(t, slug) });
    if (tags.length >= POPULAR_TAGS_LIMIT) break;
  }

  return tags;
}

async function fetchRecentViewsByCategorySlug(): Promise<string[]> {
  const admin = createAdminClient();
  if (!admin) return [];

  const since = new Date(
    Date.now() - POPULAR_TAGS_LOOKBACK_DAYS * 86400000
  ).toISOString();

  const { data, error } = await fetchAllRows<ResourceViewRow>(async (range) => {
    const result = await admin
      .from("resource_views")
      .select("resource:resources(category:categories(slug))")
      .gte("viewed_at", since)
      .range(range.from, range.to);

    return {
      data: (result.data ?? []) as unknown as ResourceViewRow[],
      error: result.error,
    };
  });

  if (error) return [];

  const counts = new Map<string, number>();
  for (const row of data) {
    const slug = row.resource?.category?.slug;
    if (!slug) continue;
    counts.set(slug, (counts.get(slug) ?? 0) + 1);
  }

  return topSlugsFromCounts(counts);
}

async function fetchViewCountsByCategorySlug(): Promise<string[]> {
  const supabase = await createClient();
  if (!supabase) return [];

  const { data, error } = await fetchAllRows<ResourceViewCountRow>(async (range) => {
    const result = await supabase
      .from("resources")
      .select("view_count, category:categories(slug)")
      .eq("status", "active")
      .gt("view_count", 0)
      .range(range.from, range.to);

    return {
      data: (result.data ?? []) as unknown as ResourceViewCountRow[],
      error: result.error,
    };
  });

  if (error) return [];

  const counts = new Map<string, number>();
  for (const row of data) {
    const slug = row.category?.slug;
    if (!slug) continue;
    counts.set(slug, (counts.get(slug) ?? 0) + row.view_count);
  }

  return topSlugsFromCounts(counts);
}

export async function getPopularCategorySlugs(): Promise<string[]> {
  if (!isSupabaseConfigured()) {
    return [...DEFAULT_POPULAR_CATEGORY_SLUGS];
  }

  if (isAdminClientConfigured()) {
    const recentSlugs = await fetchRecentViewsByCategorySlug();
    if (recentSlugs.length >= POPULAR_TAGS_LIMIT) {
      return recentSlugs;
    }
  }

  const viewCountSlugs = await fetchViewCountsByCategorySlug();
  if (viewCountSlugs.length >= POPULAR_TAGS_LIMIT) {
    return viewCountSlugs;
  }

  if (viewCountSlugs.length > 0) {
    return viewCountSlugs;
  }

  return [...DEFAULT_POPULAR_CATEGORY_SLUGS];
}
