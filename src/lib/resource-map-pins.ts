import type { Resource } from "@/types";
import { isStatewideResource } from "@/lib/resource-coverage";
import { COUNTY_CENTROIDS } from "@/lib/us-map/county-centroids.generated";
import { US_STATE_MAP_PATHS } from "@/lib/us-map/state-paths.generated";
import { projectLatLonToMap } from "@/lib/us-map/projection";

export interface ResourceMapPin {
  state: string;
  county: string;
  resourceCount: number;
  x: number;
  y: number;
}

export interface ResourceMapStateSummary {
  state: string;
  resourceCount: number;
  countyCount: number;
}

const countyCentroidByKey = new Map(
  COUNTY_CENTROIDS.map((centroid) => [`${centroid.state}|${centroid.county}`, centroid])
);

const stateCentroidByName = new Map(US_STATE_MAP_PATHS.map((state) => [state.name, state]));

function addCountyCount(
  counts: Map<string, number>,
  state: string,
  county: string,
  amount = 1
): void {
  const normalizedCounty = county.trim();
  if (!normalizedCounty) return;
  const key = `${state}|${normalizedCounty}`;
  counts.set(key, (counts.get(key) ?? 0) + amount);
}

export function buildResourceMapPins(resources: Resource[]): ResourceMapPin[] {
  const countyCounts = new Map<string, number>();
  const stateTotals = new Map<string, number>();
  const statesWithLocalCoverage = new Set<string>();

  for (const resource of resources) {
    if (resource.status !== "active") continue;

    const state = resource.state?.trim();
    if (!state) continue;

    stateTotals.set(state, (stateTotals.get(state) ?? 0) + 1);

    if (isStatewideResource(resource)) continue;

    const counties = new Set<string>();
    for (const county of resource.served_counties ?? []) {
      if (county.trim()) counties.add(county.trim());
    }
    if (resource.county?.trim()) counties.add(resource.county.trim());

    if (counties.size === 0) continue;

    statesWithLocalCoverage.add(state);
    for (const county of counties) {
      addCountyCount(countyCounts, state, county);
    }
  }

  const pins: ResourceMapPin[] = [];

  for (const [key, resourceCount] of countyCounts) {
    const centroid = countyCentroidByKey.get(key);
    if (!centroid) continue;

    const [state, county] = key.split("|");
    const { x, y } = projectLatLonToMap(centroid.lon, centroid.lat);
    pins.push({ state, county, resourceCount, x, y });
  }

  for (const [state, resourceCount] of stateTotals) {
    if (statesWithLocalCoverage.has(state)) continue;

    const stateCentroid = stateCentroidByName.get(state);
    if (!stateCentroid) continue;

    pins.push({
      state,
      county: "",
      resourceCount,
      x: stateCentroid.x,
      y: stateCentroid.y,
    });
  }

  return pins.sort((a, b) => {
    const stateDiff = a.state.localeCompare(b.state);
    if (stateDiff !== 0) return stateDiff;
    return a.county.localeCompare(b.county);
  });
}

export function buildResourceMapStateSummaries(resources: Resource[]): ResourceMapStateSummary[] {
  const pins = buildResourceMapPins(resources);
  const countyCountsByState = new Map<string, Set<string>>();
  const resourceCountsByState = new Map<string, number>();

  for (const resource of resources) {
    if (resource.status !== "active") continue;
    const state = resource.state?.trim();
    if (!state) continue;
    resourceCountsByState.set(state, (resourceCountsByState.get(state) ?? 0) + 1);
  }

  for (const pin of pins) {
    if (!pin.county) continue;
    const counties = countyCountsByState.get(pin.state) ?? new Set<string>();
    counties.add(pin.county);
    countyCountsByState.set(pin.state, counties);
  }

  return [...resourceCountsByState.entries()]
    .map(([state, resourceCount]) => ({
      state,
      resourceCount,
      countyCount: countyCountsByState.get(state)?.size ?? 0,
    }))
    .sort((a, b) => a.state.localeCompare(b.state));
}

export function getActiveResourceMapStates(resources: Resource[]): Set<string> {
  return new Set(
    resources
      .filter((resource) => resource.status === "active" && resource.state?.trim())
      .map((resource) => resource.state!.trim())
  );
}

export function resourceMapPinRadius(resourceCount: number): number {
  if (resourceCount <= 1) return 1.5;
  if (resourceCount <= 3) return 1.75;
  if (resourceCount <= 8) return 2;
  if (resourceCount <= 20) return 2.25;
  return 2.5;
}
