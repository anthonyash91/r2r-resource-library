import type { Resource } from "@/types";
import { normalizeService } from "@/lib/service-types";

export interface LocationCatalog {
  cities: string[];
  counties: string[];
  states: string[];
}

export interface ResolvedSearch {
  city?: string;
  county?: string;
  state?: string;
  textQuery?: string;
}

const STATE_ABBREVIATIONS: Record<string, string> = {
  al: "Alabama",
  ak: "Alaska",
  az: "Arizona",
  ar: "Arkansas",
  ca: "California",
  co: "Colorado",
  ct: "Connecticut",
  de: "Delaware",
  fl: "Florida",
  ga: "Georgia",
  hi: "Hawaii",
  id: "Idaho",
  il: "Illinois",
  in: "Indiana",
  ia: "Iowa",
  ks: "Kansas",
  ky: "Kentucky",
  la: "Louisiana",
  me: "Maine",
  md: "Maryland",
  ma: "Massachusetts",
  mi: "Michigan",
  mn: "Minnesota",
  ms: "Mississippi",
  mo: "Missouri",
  mt: "Montana",
  ne: "Nebraska",
  nv: "Nevada",
  nh: "New Hampshire",
  nj: "New Jersey",
  nm: "New Mexico",
  ny: "New York",
  nc: "North Carolina",
  nd: "North Dakota",
  oh: "Ohio",
  ok: "Oklahoma",
  or: "Oregon",
  pa: "Pennsylvania",
  ri: "Rhode Island",
  sc: "South Carolina",
  sd: "South Dakota",
  tn: "Tennessee",
  tx: "Texas",
  ut: "Utah",
  vt: "Vermont",
  va: "Virginia",
  wa: "Washington",
  wv: "West Virginia",
  wi: "Wisconsin",
  wy: "Wyoming",
  dc: "District of Columbia",
};

export function buildLocationCatalog(resources: Resource[]): LocationCatalog {
  return {
    cities: [...new Set(resources.map((r) => r.city).filter(Boolean) as string[])].sort(),
    counties: [...new Set(resources.map((r) => r.county).filter(Boolean) as string[])].sort(),
    states: [...new Set(resources.map((r) => r.state).filter(Boolean) as string[])].sort(),
  };
}

export function normalizeSearchQuery(query: string): string {
  return query.trim().replace(/\s+/g, " ");
}

function stripCountySuffix(value: string): string {
  return value.replace(/\s+county$/i, "").trim();
}

function findStateMatch(input: string, states: string[]): string | undefined {
  const lower = input.toLowerCase();
  const fromAbbrev = STATE_ABBREVIATIONS[lower];
  if (fromAbbrev) {
    return states.find((state) => state.toLowerCase() === fromAbbrev.toLowerCase()) ?? fromAbbrev;
  }
  return states.find((state) => state.toLowerCase() === lower);
}

function findCityMatch(input: string, cities: string[]): string | undefined {
  const lower = input.toLowerCase();
  return cities.find((city) => city.toLowerCase() === lower);
}

function findCountyMatch(input: string, counties: string[]): string | undefined {
  const lower = input.toLowerCase();
  const withoutSuffix = stripCountySuffix(input).toLowerCase();
  return counties.find(
    (county) => county.toLowerCase() === lower || county.toLowerCase() === withoutSuffix
  );
}

function matchLeadingLocation(
  query: string,
  catalog: LocationCatalog
): ResolvedSearch | null {
  const qLower = query.toLowerCase();

  for (const city of [...catalog.cities].sort((a, b) => b.length - a.length)) {
    const cityLower = city.toLowerCase();
    if (qLower.startsWith(`${cityLower} `)) {
      return { city, textQuery: query.slice(city.length).trim() };
    }
    if (qLower.endsWith(` ${cityLower}`)) {
      return { city, textQuery: query.slice(0, query.length - city.length).trim() };
    }
  }

  for (const county of [...catalog.counties].sort((a, b) => b.length - a.length)) {
    const countyLower = county.toLowerCase();
    const countyLabel = `${countyLower} county`;
    if (qLower.startsWith(`${countyLabel} `)) {
      return { county, textQuery: query.slice(countyLabel.length).trim() };
    }
    if (qLower.startsWith(`${countyLower} `)) {
      return { county, textQuery: query.slice(county.length).trim() };
    }
    if (qLower.endsWith(` ${countyLabel}`) || qLower.endsWith(` ${countyLower}`)) {
      const suffix = qLower.endsWith(` ${countyLabel}`) ? countyLabel : countyLower;
      return { county, textQuery: query.slice(0, query.length - suffix.length).trim() };
    }
  }

  return null;
}

export function resolveSearchQuery(query: string, catalog: LocationCatalog): ResolvedSearch {
  const normalized = normalizeSearchQuery(query);
  if (!normalized) return {};

  const commaMatch = normalized.match(/^(.+?),\s*(.+)$/);
  if (commaMatch) {
    const place = commaMatch[1].trim();
    const statePart = commaMatch[2].trim();
    const state = findStateMatch(statePart, catalog.states);
    const city = findCityMatch(place, catalog.cities);
    if (city) {
      return { city, ...(state ? { state } : {}) };
    }
    const county = findCountyMatch(place, catalog.counties);
    if (county) {
      return { county, ...(state ? { state } : {}) };
    }
  }

  const state = findStateMatch(normalized, catalog.states);
  if (state) return { state };

  const city = findCityMatch(normalized, catalog.cities);
  if (city) return { city };

  const county = findCountyMatch(normalized, catalog.counties);
  if (county) return { county };

  const leadingLocation = matchLeadingLocation(normalized, catalog);
  if (leadingLocation) return leadingLocation;

  return { textQuery: normalized };
}

function categoryMatchesQuery(
  category: Resource["category"],
  textQuery: string
): boolean {
  if (!category) return false;

  const q = textQuery.toLowerCase();
  const slug = category.slug.toLowerCase();
  const slugSpaced = slug.replace(/-/g, " ");

  return (
    category.name.toLowerCase().includes(q) ||
    slug.includes(q) ||
    slugSpaced.includes(q) ||
    (category.description?.toLowerCase().includes(q) ?? false)
  );
}

export function resourceMatchesTextQuery(resource: Resource, textQuery: string): boolean {
  const q = textQuery.toLowerCase();
  return (
    categoryMatchesQuery(resource.category, textQuery) ||
    resource.name.toLowerCase().includes(q) ||
    resource.description.toLowerCase().includes(q) ||
    resource.services.some((service) => normalizeService(service).toLowerCase().includes(q)) ||
    resource.tags.some((tag) => tag.toLowerCase().includes(q)) ||
    (resource.eligibility?.toLowerCase().includes(q) ?? false) ||
    (resource.notes?.toLowerCase().includes(q) ?? false) ||
    (resource.city?.toLowerCase().includes(q) ?? false) ||
    (resource.county?.toLowerCase().includes(q) ?? false) ||
    (resource.state?.toLowerCase().includes(q) ?? false) ||
    (resource.address?.toLowerCase().includes(q) ?? false)
  );
}

export function applySearchQueryFilter(
  resources: Resource[],
  query: string | undefined,
  catalog: LocationCatalog
): Resource[] {
  if (!query?.trim()) return resources;

  const resolved = resolveSearchQuery(query, catalog);
  let results = resources;

  if (resolved.state) {
    results = results.filter((resource) => resource.state === resolved.state);
  }
  if (resolved.county) {
    results = results.filter((resource) => resource.county === resolved.county);
  }
  if (resolved.city) {
    results = results.filter((resource) => resource.city === resolved.city);
  }

  if (resolved.textQuery) {
    results = results.filter((resource) => resourceMatchesTextQuery(resource, resolved.textQuery!));
  } else if (!resolved.city && !resolved.county && !resolved.state) {
    results = results.filter((resource) => resourceMatchesTextQuery(resource, query.trim()));
  }

  return results;
}

export function escapeIlikePattern(value: string): string {
  return value.replace(/[%_,]/g, "\\$&");
}
