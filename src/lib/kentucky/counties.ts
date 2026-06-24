/** Canonical Kentucky county names (120 counties) for filters and validation. */
export const KENTUCKY_COUNTIES = [
  "Adair",
  "Allen",
  "Anderson",
  "Ballard",
  "Barren",
  "Bath",
  "Bell",
  "Boone",
  "Bourbon",
  "Boyd",
  "Boyle",
  "Bracken",
  "Breathitt",
  "Breckinridge",
  "Bullitt",
  "Butler",
  "Caldwell",
  "Calloway",
  "Campbell",
  "Carlisle",
  "Carroll",
  "Carter",
  "Casey",
  "Christian",
  "Clark",
  "Clay",
  "Clinton",
  "Crittenden",
  "Cumberland",
  "Daviess",
  "Edmonson",
  "Elliott",
  "Estill",
  "Fayette",
  "Fleming",
  "Floyd",
  "Franklin",
  "Fulton",
  "Gallatin",
  "Garrard",
  "Grant",
  "Graves",
  "Grayson",
  "Green",
  "Greenup",
  "Hancock",
  "Hardin",
  "Harlan",
  "Harrison",
  "Hart",
  "Henderson",
  "Henry",
  "Hickman",
  "Hopkins",
  "Jackson",
  "Jefferson",
  "Jessamine",
  "Johnson",
  "Kenton",
  "Knott",
  "Knox",
  "Larue",
  "Laurel",
  "Lawrence",
  "Lee",
  "Leslie",
  "Letcher",
  "Lewis",
  "Lincoln",
  "Livingston",
  "Logan",
  "Lyon",
  "Madison",
  "Magoffin",
  "Marion",
  "Martin",
  "Marshall",
  "Mason",
  "McCracken",
  "McCreary",
  "McLean",
  "Meade",
  "Menifee",
  "Mercer",
  "Metcalfe",
  "Monroe",
  "Montgomery",
  "Morgan",
  "Muhlenberg",
  "Nelson",
  "Nicholas",
  "Ohio",
  "Oldham",
  "Owen",
  "Owsley",
  "Pendleton",
  "Perry",
  "Pike",
  "Powell",
  "Pulaski",
  "Robertson",
  "Rockcastle",
  "Rowan",
  "Russell",
  "Scott",
  "Shelby",
  "Simpson",
  "Spencer",
  "Taylor",
  "Todd",
  "Trigg",
  "Trimble",
  "Union",
  "Warren",
  "Washington",
  "Wayne",
  "Webster",
  "Whitley",
  "Wolfe",
  "Woodford",
] as const;

export type KentuckyCounty = (typeof KENTUCKY_COUNTIES)[number];

const COUNTY_LOOKUP = new Map(
  KENTUCKY_COUNTIES.map((c) => [c.toLowerCase(), c] as const)
);

export function normalizeCountyName(value: string): KentuckyCounty | null {
  const trimmed = value.trim().replace(/\s+County$/i, "");
  if (!trimmed) return null;
  const key = trimmed.toLowerCase().replace(/\s+/g, "");
  if (key === "larue") return "Larue";
  return COUNTY_LOOKUP.get(trimmed.toLowerCase()) ?? null;
}

export function parseCountyList(value: string): KentuckyCounty[] {
  if (!value.trim()) return [];
  const seen = new Set<string>();
  const out: KentuckyCounty[] = [];
  for (const part of value.split(/[|,]/)) {
    const county = normalizeCountyName(part);
    if (county && !seen.has(county)) {
      seen.add(county);
      out.push(county);
    }
  }
  return out;
}
