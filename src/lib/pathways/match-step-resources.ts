import { resolveCategoryMessageSlug } from "@/i18n/category-label";
import { isStatewideResource, resourceServesCounty } from "@/lib/resource-coverage";
import type { Resource } from "@/types";
import type { UserPreferences } from "@/lib/user-preferences/types";
import type { MatchedPathwayStep, PathwayDef, PathwayStepDef } from "./types";

function categorySlug(resource: Resource): string | null {
  const raw = resource.category?.slug;
  if (!raw) return null;
  return resolveCategoryMessageSlug(raw);
}

function resourceMatchesTags(resource: Resource, tagSlugs: string[]): boolean {
  if (!tagSlugs.length) return false;
  const normalized = resource.tags.map((tag) => tag.toLowerCase());
  return tagSlugs.some((slug) =>
    normalized.some((tag) => tag === slug || tag.includes(slug))
  );
}

function resourceMatchesStep(resource: Resource, step: PathwayStepDef): boolean {
  const slug = categorySlug(resource);
  const categoryMatch =
    Boolean(step.categorySlugs?.length) &&
    slug !== null &&
    step.categorySlugs!.includes(slug);
  const tagMatch = resourceMatchesTags(resource, step.tagSlugs ?? []);

  if (step.categorySlugs?.length && step.tagSlugs?.length) {
    return categoryMatch || tagMatch;
  }
  if (step.categorySlugs?.length) return categoryMatch;
  if (step.tagSlugs?.length) return tagMatch;
  return false;
}

function stepMatchesUserPriority(step: PathwayStepDef, prioritySlugs: string[]): boolean {
  if (!prioritySlugs.length || !step.categorySlugs?.length) return false;
  return step.categorySlugs.some((slug) => prioritySlugs.includes(slug));
}

function compareStepResources(a: Resource, b: Resource): number {
  if (a.is_featured !== b.is_featured) {
    return a.is_featured ? -1 : 1;
  }
  if (b.view_count !== a.view_count) {
    return b.view_count - a.view_count;
  }
  return a.name.localeCompare(b.name);
}

function selectStepResources(
  candidates: Resource[],
  step: PathwayStepDef,
  county: string | null
): Resource[] {
  const local = candidates
    .filter((resource) => !isStatewideResource(resource))
    .sort(compareStepResources);
  const statewide = step.includeStatewide
    ? candidates.filter((resource) => isStatewideResource(resource)).sort(compareStepResources)
    : [];

  const ordered = step.preferStatewide
    ? [...statewide, ...local]
    : [...local, ...statewide];

  const selected: Resource[] = [];
  const used = new Set<string>();

  for (const resource of ordered) {
    if (selected.length >= step.maxResources) break;
    if (used.has(resource.id)) continue;
    selected.push(resource);
    used.add(resource.id);
  }

  if (!county) {
    return selected;
  }

  return selected;
}

export function matchStepResources(
  allResources: Resource[],
  step: PathwayStepDef,
  prefs: UserPreferences | null
): MatchedPathwayStep {
  const county = prefs?.county?.trim() || null;
  const state = prefs?.state?.trim() || null;
  const prioritySlugs = prefs?.priorityCategories ?? [];

  let candidates = allResources.filter((resource) => resource.status === "active");

  if (state) {
    candidates = candidates.filter(
      (resource) => !resource.state || resource.state === state
    );
  }

  candidates = candidates.filter((resource) => resourceMatchesStep(resource, step));

  if (county) {
    candidates = candidates.filter((resource) => resourceServesCounty(resource, county));
  }

  const resources = selectStepResources(candidates, step, county);
  const localResources = resources.filter((resource) => !isStatewideResource(resource));
  const statewideResources = resources.filter((resource) => isStatewideResource(resource));

  return {
    step,
    resources,
    localResources,
    statewideResources,
    matchesUserPriority: stepMatchesUserPriority(step, prioritySlugs),
  };
}

export function matchPathwaySteps(
  allResources: Resource[],
  pathway: PathwayDef,
  prefs: UserPreferences | null
): MatchedPathwayStep[] {
  return pathway.stepIds.map((step) => matchStepResources(allResources, step, prefs));
}
