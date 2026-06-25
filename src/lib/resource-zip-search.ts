import type { Resource } from "@/types";
import { COUNTY_CENTROIDS } from "@/lib/us-map/county-centroids.generated";
import { isStatewideResource, resourceServesCounty } from "@/lib/resource-coverage";

export interface ZipLocation {
  zip: string;
  city: string;
  state: string;
  lat: number;
  lon: number;
  county: string;
}

/** Resources in the same ZIP area (city match or within this radius). */
export const IN_ZIP_RADIUS_MILES = 8;

/** Regional resources shown after in-ZIP results. */
export const NEAR_ZIP_RADIUS_MILES = 50;

const countyCentroidByKey = new Map(
  COUNTY_CENTROIDS.map((centroid) => [`${centroid.state}|${centroid.county}`, centroid])
);

export function haversineMiles(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const earthRadiusMiles = 3958.8;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return earthRadiusMiles * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function resolveZipCounty(location: {
  state: string;
  lat: number;
  lon: number;
}): string {
  let bestCounty = "";
  let bestDistance = Infinity;

  for (const centroid of COUNTY_CENTROIDS) {
    if (centroid.state !== location.state) continue;
    const distance = haversineMiles(location.lat, location.lon, centroid.lat, centroid.lon);
    if (distance < bestDistance) {
      bestDistance = distance;
      bestCounty = centroid.county;
    }
  }

  return bestCounty;
}

function normalizeCity(city: string): string {
  return city.toLowerCase().replace(/\s+/g, " ").trim();
}

export function getResourceGeoPoint(resource: Resource): { lat: number; lon: number } | null {
  const state = resource.state?.trim();
  if (!state) return null;

  const counties = new Set<string>();
  if (resource.county?.trim()) counties.add(resource.county.trim());
  for (const county of resource.served_counties ?? []) {
    if (county.trim()) counties.add(county.trim());
  }

  for (const county of counties) {
    const centroid = countyCentroidByKey.get(`${state}|${county}`);
    if (centroid) return { lat: centroid.lat, lon: centroid.lon };
  }

  return null;
}

function resourceMatchesZipCity(resource: Resource, zip: ZipLocation): boolean {
  if (!resource.city?.trim() || resource.state !== zip.state) return false;
  return normalizeCity(resource.city) === normalizeCity(zip.city);
}

function distanceMilesFromZip(resource: Resource, zip: ZipLocation): number | null {
  const point = getResourceGeoPoint(resource);
  if (!point) return null;
  return haversineMiles(zip.lat, zip.lon, point.lat, point.lon);
}

export interface ZipPartitionedResources {
  inZip: Resource[];
  nearZip: Resource[];
  statewide: Resource[];
}

export function partitionResourcesByZip(
  resources: Resource[],
  zip: ZipLocation
): ZipPartitionedResources {
  const inZip: Resource[] = [];
  const nearZip: Resource[] = [];
  const statewide: Resource[] = [];

  for (const resource of resources) {
    if (resource.state !== zip.state) continue;

    if (isStatewideResource(resource)) {
      statewide.push(resource);
      continue;
    }

    const distance = distanceMilesFromZip(resource, zip);
    if (distance == null) continue;

    const servesZipCounty = resourceServesCounty(resource, zip.county);
    const inZipMatch = resourceMatchesZipCity(resource, zip) || distance <= IN_ZIP_RADIUS_MILES;

    if (inZipMatch && (servesZipCounty || distance <= IN_ZIP_RADIUS_MILES)) {
      inZip.push(resource);
      continue;
    }

    if (distance <= NEAR_ZIP_RADIUS_MILES && (servesZipCounty || distance <= NEAR_ZIP_RADIUS_MILES)) {
      nearZip.push(resource);
    }
  }

  const sortByDistance = (a: Resource, b: Resource) => {
    const da = distanceMilesFromZip(a, zip) ?? Infinity;
    const db = distanceMilesFromZip(b, zip) ?? Infinity;
    return da - db;
  };

  inZip.sort(sortByDistance);
  nearZip.sort(sortByDistance);

  return { inZip, nearZip, statewide };
}

export function flattenZipPartition(partition: ZipPartitionedResources): Resource[] {
  return [...partition.inZip, ...partition.nearZip, ...partition.statewide];
}
