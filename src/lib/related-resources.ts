import type { Resource } from "@/types";
import { isStatewideResource, resourceServesCounty } from "@/lib/resource-coverage";
import { normalizeService } from "@/lib/service-types";

function referenceCounties(resource: Resource): string[] {
  const counties = new Set<string>();
  if (resource.county?.trim()) counties.add(resource.county.trim());
  for (const county of resource.served_counties ?? []) {
    if (county.trim()) counties.add(county.trim());
  }
  return [...counties];
}

/** Lower score = more geographically relevant to the reference resource. */
export function relatedResourceCountyScore(
  candidate: Resource,
  referenceCounties: string[]
): number {
  if (referenceCounties.length === 0) return 2;

  let best = 4;
  for (const county of referenceCounties) {
    if (isStatewideResource(candidate)) {
      best = Math.min(best, 2);
      continue;
    }
    if (candidate.county === county) {
      best = Math.min(best, 0);
      continue;
    }
    if (candidate.served_counties?.includes(county)) {
      best = Math.min(best, 1);
      continue;
    }
    if (resourceServesCounty(candidate, county)) {
      best = Math.min(best, 1);
    }
  }
  return best;
}

function sharedTagCount(reference: Resource, candidate: Resource): number {
  const tags = new Set(reference.tags.map((tag) => tag.toLowerCase()));
  return candidate.tags.filter((tag) => tags.has(tag.toLowerCase())).length;
}

function sharedServiceCount(reference: Resource, candidate: Resource): number {
  const services = new Set(
    reference.services.map((service) => normalizeService(service).toLowerCase())
  );
  return candidate.services.filter((service) =>
    services.has(normalizeService(service).toLowerCase())
  ).length;
}

/**
 * Rank same-category candidates for a resource detail page:
 * 1. Same state only (when the reference has a state).
 * 2. County / service-area relevance (local → regional → statewide in-state).
 * 3. Shared tags and services as tie-breakers.
 * 4. Alphabetical by name.
 */
export function pickRelatedResources(
  resource: Resource,
  candidates: Resource[],
  limit = 4
): Resource[] {
  const state = resource.state?.trim();
  const pool = candidates.filter(
    (candidate) =>
      candidate.id !== resource.id &&
      candidate.status === "active" &&
      (!state || candidate.state === state)
  );

  if (pool.length === 0) return [];

  const counties = referenceCounties(resource);
  const referenceCity = resource.city?.trim();

  return [...pool]
    .sort((a, b) => {
      const countyDiff =
        relatedResourceCountyScore(a, counties) - relatedResourceCountyScore(b, counties);
      if (countyDiff !== 0) return countyDiff;

      if (counties.length === 0 && referenceCity) {
        const aCityMatch = a.city === referenceCity ? 0 : 1;
        const bCityMatch = b.city === referenceCity ? 0 : 1;
        if (aCityMatch !== bCityMatch) return aCityMatch - bCityMatch;
      }

      const tagDiff = sharedTagCount(resource, b) - sharedTagCount(resource, a);
      if (tagDiff !== 0) return tagDiff;

      const serviceDiff =
        sharedServiceCount(resource, b) - sharedServiceCount(resource, a);
      if (serviceDiff !== 0) return serviceDiff;

      return a.name.localeCompare(b.name);
    })
    .slice(0, limit);
}
