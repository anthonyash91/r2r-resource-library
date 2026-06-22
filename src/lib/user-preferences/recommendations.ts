import type { Resource } from "@/types";
import { resolveCategoryMessageSlug } from "@/i18n/category-label";
import { isStatewideResource, resourceServesCounty } from "@/lib/resource-coverage";
import type { UserPreferences } from "./types";

const DEFAULT_LIMIT = 6;

function categorySlug(resource: Resource): string | null {
  const raw = resource.category?.slug;
  if (!raw) return null;
  return resolveCategoryMessageSlug(raw);
}

function matchesPriority(resource: Resource, prioritySlugs: string[]): boolean {
  const slug = categorySlug(resource);
  return slug !== null && prioritySlugs.includes(slug);
}

/** Lower is a better match; non-matches sort last. Respects user's selection order. */
function priorityRank(resource: Resource, prioritySlugs: string[]): number {
  if (!prioritySlugs.length) return 0;
  const slug = categorySlug(resource);
  if (!slug) return prioritySlugs.length + 1;
  const index = prioritySlugs.indexOf(slug);
  return index === -1 ? prioritySlugs.length + 1 : index;
}

/** Lower is more relevant within the local tier (in-county before regional). */
function localCountyScore(resource: Resource, county: string): number {
  if (resource.county === county) return 0;
  if (resource.served_counties?.includes(county)) return 1;
  return 2;
}

function compareRecommendations(
  a: Resource,
  b: Resource,
  county: string,
  prioritySlugs: string[]
): number {
  const priorityDiff = priorityRank(a, prioritySlugs) - priorityRank(b, prioritySlugs);
  if (priorityDiff !== 0) return priorityDiff;

  const countyDiff = localCountyScore(a, county) - localCountyScore(b, county);
  if (countyDiff !== 0) return countyDiff;

  if (a.is_featured !== b.is_featured) {
    return a.is_featured ? -1 : 1;
  }

  if (b.view_count !== a.view_count) {
    return b.view_count - a.view_count;
  }

  return a.name.localeCompare(b.name);
}

function sortRecommendations(
  resources: Resource[],
  county: string,
  prioritySlugs: string[]
): Resource[] {
  return [...resources].sort((a, b) => compareRecommendations(a, b, county, prioritySlugs));
}

function pickBest(
  candidates: Resource[],
  county: string,
  prioritySlugs: string[],
  used: Set<string>
): Resource | undefined {
  return sortRecommendations(
    candidates.filter((resource) => !used.has(resource.id)),
    county,
    prioritySlugs
  )[0];
}

export function getRecommendedResources(
  resources: Resource[],
  prefs: UserPreferences | null,
  limit = DEFAULT_LIMIT
): Resource[] {
  const active = resources.filter((r) => r.status === "active");
  const county = prefs?.county?.trim();
  const state = prefs?.state?.trim();
  const priorityCategories = prefs?.priorityCategories ?? [];

  if (!county || !state) {
    return [...active].sort((a, b) => b.view_count - a.view_count).slice(0, limit);
  }

  const serving = active.filter((resource) => {
    if (resource.state && resource.state !== state) return false;
    return resourceServesCounty(resource, county);
  });

  const local = serving.filter((resource) => !isStatewideResource(resource));
  const statewide = serving.filter((resource) => isStatewideResource(resource));
  const result: Resource[] = [];
  const used = new Set<string>();

  // Reserve a slot per selected need when possible (local before statewide).
  for (const slug of priorityCategories) {
    if (result.length >= limit) break;

    const localPick = pickBest(
      local.filter((resource) => categorySlug(resource) === slug),
      county,
      priorityCategories,
      used
    );
    if (localPick) {
      result.push(localPick);
      used.add(localPick.id);
      continue;
    }

    const statewidePick = pickBest(
      statewide.filter((resource) => categorySlug(resource) === slug),
      county,
      priorityCategories,
      used
    );
    if (statewidePick) {
      result.push(statewidePick);
      used.add(statewidePick.id);
    }
  }

  const matchingLocal = local.filter(
    (resource) => matchesPriority(resource, priorityCategories) && !used.has(resource.id)
  );
  const matchingStatewide = statewide.filter(
    (resource) => matchesPriority(resource, priorityCategories) && !used.has(resource.id)
  );
  const otherLocal = local.filter(
    (resource) => !matchesPriority(resource, priorityCategories) && !used.has(resource.id)
  );
  const otherStatewide = statewide.filter(
    (resource) => !matchesPriority(resource, priorityCategories) && !used.has(resource.id)
  );

  const fillOrder =
    priorityCategories.length > 0
      ? [
          ...sortRecommendations(matchingLocal, county, priorityCategories),
          ...sortRecommendations(matchingStatewide, county, priorityCategories),
          ...sortRecommendations(otherLocal, county, priorityCategories),
          ...sortRecommendations(otherStatewide, county, priorityCategories),
        ]
      : [
          ...sortRecommendations(local, county, priorityCategories),
          ...sortRecommendations(statewide, county, priorityCategories),
        ];

  for (const resource of fillOrder) {
    if (result.length >= limit) break;
    if (used.has(resource.id)) continue;
    result.push(resource);
    used.add(resource.id);
  }

  return result;
}
