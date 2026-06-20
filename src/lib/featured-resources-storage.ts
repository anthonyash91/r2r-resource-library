import type { Resource } from "@/types";

export const FEATURED_RESOURCES_KEY = "reentry_featured_resources";
export const MAX_FEATURED_RESOURCES = 3;

export function getStoredFeaturedIds(): string[] | null {
  if (typeof window === "undefined") return null;

  const stored = localStorage.getItem(FEATURED_RESOURCES_KEY);
  if (!stored) return null;

  try {
    const parsed = JSON.parse(stored) as unknown;
    return Array.isArray(parsed) ? parsed.filter((id): id is string => typeof id === "string") : null;
  } catch {
    return null;
  }
}

export function setStoredFeaturedIds(ids: string[]): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(FEATURED_RESOURCES_KEY, JSON.stringify(ids.slice(0, MAX_FEATURED_RESOURCES)));
  window.dispatchEvent(new Event("featured-resources-updated"));
}

export function resolveFeaturedResources(resources: Resource[]): Resource[] {
  const storedIds = getStoredFeaturedIds();

  if (storedIds !== null) {
    const byId = new Map(resources.map((resource) => [resource.id, resource]));
    return storedIds
      .map((id) => byId.get(id))
      .filter((resource): resource is Resource => Boolean(resource && resource.status === "active"));
  }

  return resources.filter((resource) => resource.is_featured && resource.status === "active");
}

export function getFeaturedIdsFromResources(resources: Resource[]): string[] {
  return resolveFeaturedResources(resources).map((resource) => resource.id);
}

export function toggleStoredFeaturedId(resources: Resource[], id: string): string[] {
  const currentIds = getFeaturedIdsFromResources(resources);

  if (currentIds.includes(id)) {
    const nextIds = currentIds.filter((currentId) => currentId !== id);
    setStoredFeaturedIds(nextIds);
    return nextIds;
  }

  if (currentIds.length >= MAX_FEATURED_RESOURCES) {
    return currentIds;
  }

  const nextIds = [...currentIds, id];
  setStoredFeaturedIds(nextIds);
  return nextIds;
}

export function setStoredFeaturedFromFlag(resources: Resource[], id: string, featured: boolean): string[] {
  const currentIds = getFeaturedIdsFromResources(resources);

  if (featured) {
    if (currentIds.includes(id)) return currentIds;
    if (currentIds.length >= MAX_FEATURED_RESOURCES) return currentIds;
    const nextIds = [...currentIds, id];
    setStoredFeaturedIds(nextIds);
    return nextIds;
  }

  const nextIds = currentIds.filter((currentId) => currentId !== id);
  setStoredFeaturedIds(nextIds);
  return nextIds;
}
