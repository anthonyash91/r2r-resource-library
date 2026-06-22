import type { Resource, ResourceCoverage } from "@/types";
import { buildResourcesPageHref } from "@/lib/resources-page";

export function isStatewideResource(
  resource: Pick<Resource, "coverage" | "tags">
): boolean {
  if (resource.coverage === "statewide") return true;
  if (resource.coverage) return false;
  return resource.tags.some((tag) => tag.toLowerCase() === "statewide");
}

export function isRegionalResource(
  resource: Pick<Resource, "coverage">
): boolean {
  return resource.coverage === "multi";
}

export function resourceServesCounty(resource: Resource, county: string): boolean {
  if (!county.trim()) return true;
  if (isStatewideResource(resource)) return true;
  const normalized = county.trim();
  if (resource.served_counties?.some((c) => c === normalized)) return true;
  // Legacy fallback until all rows have served_counties populated
  if (!resource.served_counties?.length && resource.county === normalized) return true;
  return false;
}

export function countyCoverageLabel(
  resource: Resource,
  selectedCounty: string | undefined,
  t: (key: string) => string
): string | null {
  if (isStatewideResource(resource)) return null;

  if (!selectedCounty) {
    if (resource.coverage === "multi") return t("resources.coverageRegional");
    return null;
  }
  if (resource.served_counties?.includes(selectedCounty)) {
    if (resource.county === selectedCounty) return t("resources.coverageInCounty");
    return t("resources.coverageRegional");
  }
  return null;
}

export function sortResourcesByCountyRelevance(
  resources: Resource[],
  county: string | undefined
): Resource[] {
  if (!county) return resources;

  const score = (resource: Resource): number => {
    if (isStatewideResource(resource)) return 2;
    if (resource.county === county) return 0;
    if (resource.served_counties?.includes(county)) return 1;
    return 3;
  };

  return [...resources].sort((a, b) => {
    const diff = score(a) - score(b);
    if (diff !== 0) return diff;
    return a.name.localeCompare(b.name);
  });
}

/** Direct county match — excludes statewide-only resources. */
export function resourceMatchesCountyDirectly(
  resource: Resource,
  county: string
): boolean {
  if (!county.trim() || isStatewideResource(resource)) return false;
  const normalized = county.trim();
  if (resource.served_counties?.some((c) => c === normalized)) return true;
  if (!resource.served_counties?.length && resource.county === normalized) return true;
  return false;
}

export function partitionResourcesByCountyFilter(
  resources: Resource[],
  county: string | undefined
): { local: Resource[]; statewide: Resource[] } {
  if (!county?.trim()) {
    return { local: resources, statewide: [] };
  }

  const normalized = county.trim();
  const local = resources.filter((r) => !isStatewideResource(r));
  const statewide = resources.filter((r) => isStatewideResource(r));

  return {
    local: sortResourcesByCountyRelevance(local, normalized),
    statewide: [...statewide].sort((a, b) => a.name.localeCompare(b.name)),
  };
}

export function formatServedCounties(counties: string[], max = 8): string {
  if (!counties.length) return "";
  if (counties.length <= max) return counties.join(", ");
  return `${counties.slice(0, max).join(", ")} +${counties.length - max} more`;
}

export function isValidCoverage(value: string): value is ResourceCoverage {
  return value === "single" || value === "multi" || value === "statewide";
}

export function shouldShowCountiesServed(
  resource: Pick<Resource, "coverage" | "served_counties">
): boolean {
  if (resource.coverage === "statewide") return true;
  return (resource.served_counties?.length ?? 0) > 0;
}

export function countiesServedLabel(resource: Resource): string {
  if (resource.coverage === "statewide") return "";
  return resource.served_counties?.join(", ") ?? "";
}

export function buildCountyFilterHref(county: string, state?: string | null): string {
  const params = new URLSearchParams();
  if (state?.trim()) params.set("state", state.trim());
  params.set("county", county);
  return buildResourcesPageHref(params, "results");
}
