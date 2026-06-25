import zipcodes from "zipcodes";
import { COUNTY_CENTROIDS } from "@/lib/us-map/county-centroids.generated";
import { isSupportedOnboardingState } from "@/lib/states/registry";
import { haversineMiles, type ZipLocation } from "@/lib/resource-zip-search";

export type { ZipLocation };

function resolveZipCounty(location: { state: string; lat: number; lon: number }): string {
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

const STATE_ABBREV_TO_NAME: Record<string, string> = {
  AL: "Alabama",
  AK: "Alaska",
  AZ: "Arizona",
  AR: "Arkansas",
  CA: "California",
  CO: "Colorado",
  CT: "Connecticut",
  DE: "Delaware",
  FL: "Florida",
  GA: "Georgia",
  HI: "Hawaii",
  ID: "Idaho",
  IL: "Illinois",
  IN: "Indiana",
  IA: "Iowa",
  KS: "Kansas",
  KY: "Kentucky",
  LA: "Louisiana",
  ME: "Maine",
  MD: "Maryland",
  MA: "Massachusetts",
  MI: "Michigan",
  MN: "Minnesota",
  MS: "Mississippi",
  MO: "Missouri",
  MT: "Montana",
  NE: "Nebraska",
  NV: "Nevada",
  NH: "New Hampshire",
  NJ: "New Jersey",
  NM: "New Mexico",
  NY: "New York",
  NC: "North Carolina",
  ND: "North Dakota",
  OH: "Ohio",
  OK: "Oklahoma",
  OR: "Oregon",
  PA: "Pennsylvania",
  RI: "Rhode Island",
  SC: "South Carolina",
  SD: "South Dakota",
  TN: "Tennessee",
  TX: "Texas",
  UT: "Utah",
  VT: "Vermont",
  VA: "Virginia",
  WA: "Washington",
  WV: "West Virginia",
  WI: "Wisconsin",
  WY: "Wyoming",
  DC: "District of Columbia",
};

function normalizeZipInput(value: string): string {
  return value.replace(/\D/g, "").slice(0, 5);
}

export function lookupZip(zip: string): ZipLocation | null {
  const normalized = normalizeZipInput(zip);
  if (normalized.length !== 5) return null;

  const hit = zipcodes.lookup(normalized);
  if (!hit?.state || hit.latitude == null || hit.longitude == null) return null;

  const state = STATE_ABBREV_TO_NAME[hit.state.toUpperCase()] ?? hit.state;
  if (!isSupportedOnboardingState(state)) return null;

  const lat = Number(hit.latitude);
  const lon = Number(hit.longitude);
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null;

  const county = resolveZipCounty({ state, lat, lon });
  return {
    zip: normalized,
    city: hit.city?.trim() || "",
    state,
    lat,
    lon,
    county,
  };
}
