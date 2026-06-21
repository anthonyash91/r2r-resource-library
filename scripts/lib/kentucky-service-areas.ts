/**
 * Official and curated Kentucky regional service areas for county coverage migration.
 * Sources: KY ADD statutory boundaries, DOC P&P district notes, CMHC regions, KCTCS/KYAE,
 * legal aid maps, food bank territories, and enrichment batch research.
 */
import {
  KENTUCKY_COUNTIES,
  normalizeCountyName,
} from "../../src/lib/kentucky/counties";

export type Coverage = "single" | "multi" | "statewide";

export type ServiceArea = { coverage: Coverage; counties: string[] };

function area(counties: string[]): ServiceArea {
  const valid = counties
    .map((c) => normalizeCountyName(c) ?? c)
    .filter((c) => (KENTUCKY_COUNTIES as readonly string[]).includes(c));
  const unique = [...new Set(valid)].sort((a, b) => a.localeCompare(b));
  if (unique.length === 0) return { coverage: "single", counties: [] };
  if (unique.length === 1) return { coverage: "single", counties: unique };
  return { coverage: "multi", counties: unique };
}

function statewide(): ServiceArea {
  return { coverage: "statewide", counties: [] };
}

/** Kentucky Area Development Districts (15 ADDs). */
export const ADD_REGIONS = {
  purchase: area([
    "Ballard", "Calloway", "Carlisle", "Fulton", "Graves", "Hickman", "Livingston",
    "Lyon", "Marshall", "McCracken",
  ]),
  pennyrile: area([
    "Caldwell", "Christian", "Crittenden", "Hopkins", "Livingston", "Lyon",
    "Muhlenberg", "Todd", "Trigg",
  ]),
  greenRiver: area([
    "Daviess", "Hancock", "Henderson", "McLean", "Ohio", "Union", "Webster",
  ]),
  barrenRiver: area([
    "Allen", "Barren", "Butler", "Edmonson", "Hart", "Logan", "Metcalfe", "Monroe",
    "Simpson", "Warren",
  ]),
  lincolnTrail: area([
    "Breckinridge", "Grayson", "Hardin", "LaRue", "Marion", "Meade", "Nelson",
    "Washington",
  ]),
  jefferson: area([
    "Bullitt", "Henry", "Jefferson", "Oldham", "Shelby", "Spencer", "Trimble",
  ]),
  northernKentucky: area([
    "Boone", "Bracken", "Campbell", "Carroll", "Gallatin", "Grant", "Kenton",
    "Owen", "Pendleton",
  ]),
  buffaloTrace: area(["Bracken", "Fleming", "Lewis", "Mason", "Robertson"]),
  gateway: area(["Bath", "Menifee", "Montgomery", "Morgan", "Rowan"]),
  fivco: area(["Boyd", "Carter", "Elliott", "Greenup", "Lawrence"]),
  bigSandy: area([
    "Floyd", "Johnson", "Knott", "Letcher", "Magoffin", "Martin", "Pike",
  ]),
  kentuckyRiver: area([
    "Breathitt", "Knott", "Lee", "Leslie", "Letcher", "Owsley", "Perry", "Wolfe",
  ]),
  cumberlandValley: area([
    "Bell", "Clay", "Harlan", "Jackson", "Knox", "Laurel", "McCreary", "Rockcastle",
    "Wayne", "Whitley",
  ]),
  lakeCumberland: area([
    "Adair", "Casey", "Clinton", "Cumberland", "Green", "McCreary", "Pulaski",
    "Russell", "Taylor", "Wayne",
  ]),
  bluegrass: area([
    "Anderson", "Bourbon", "Boyle", "Clark", "Estill", "Fayette", "Franklin",
    "Garrard", "Harrison", "Jessamine", "Lincoln", "Madison", "Mercer", "Nicholas",
    "Powell", "Scott", "Woodford",
  ]),
} as const;

/** DOC Probation & Parole district county assignments (from DOC contact pages + enrichment). */
export const PP_DISTRICTS: Record<number, ServiceArea> = {
  1: ADD_REGIONS.purchase,
  2: area([
    "Christian", "Crittenden", "Hopkins", "Livingston", "Logan", "Lyon", "Muhlenberg",
    "Simpson", "Todd", "Trigg",
  ]),
  3: area(["Adair", "Barren", "Casey", "Cumberland", "Metcalfe", "Warren"]),
  4: area(["Jefferson"]),
  5: area(["Breckinridge", "Grayson", "Hardin", "LaRue", "Marion", "Meade", "Washington"]),
  6: area(["Boyle", "Green", "LaRue", "Marion", "Mercer", "Nelson", "Taylor", "Washington"]),
  7: ADD_REGIONS.northernKentucky,
  8: area([
    "Bath", "Estill", "Madison", "Menifee", "Montgomery", "Morgan", "Powell", "Rowan",
    "Wolfe",
  ]),
  9: ADD_REGIONS.bluegrass,
  10: ADD_REGIONS.cumberlandValley,
  11: area([
    ...ADD_REGIONS.bigSandy.counties,
    "Lawrence",
  ]),
  12: area([
    "Anderson", "Carroll", "Franklin", "Henry", "Owen", "Shelby", "Trimble",
  ]),
  13: area([
    ...ADD_REGIONS.greenRiver.counties,
    "Crittenden", "Muhlenberg",
  ]),
  14: area([
    ...ADD_REGIONS.kentuckyRiver.counties,
    "Clay", "Harlan",
  ]),
  15: area([
    "Boyd", "Bracken", "Carter", "Elliott", "Fleming", "Greenup", "Lawrence", "Lewis",
    "Mason", "Morgan",
  ]),
  16: area(["Jefferson"]),
  17: area([
    "Anderson", "Bourbon", "Boyle", "Clark", "Estill", "Fayette", "Franklin", "Garrard",
    "Harrison", "Jessamine", "Lincoln", "Madison", "Mercer", "Nicholas", "Powell", "Scott",
    "Woodford",
  ]),
};

/** Map P&P office resource IDs to DOC district numbers. */
export const PP_OFFICE_DISTRICT: Record<string, number> = {
  "451": 16,
  "452": 9,
  "453": 7,
  "454": 3,
  "455": 1,
  "456": 11,
  "486": 14,
  "487": 10,
  "490": 5,
  "493": 12,
  "496": 2,
  "509": 13,
  "510": 15,
  "532": 6,
};

/** EKCEP / Eastern Kentucky CEP workforce region. */
export const EKCEP_REGION = area([
  "Bell", "Breathitt", "Carter", "Clay", "Elliott", "Floyd", "Harlan", "Jackson",
  "Johnson", "Knott", "Knox", "Lawrence", "Lee", "Leslie", "Letcher", "Magoffin",
  "Martin", "Menifee", "Morgan", "Owsley", "Perry", "Pike", "Wolfe",
]);

/** AppalReD Legal Aid (Eastern KY). */
export const APPALRED_REGION = area([
  "Adair", "Bell", "Breathitt", "Casey", "Clark", "Clay", "Clinton", "Cumberland",
  "Estill", "Floyd", "Garrard", "Harlan", "Jackson", "Johnson", "Knott", "Knox",
  "Laurel", "Lawrence", "Lee", "Leslie", "Letcher", "Lincoln", "Madison", "Magoffin",
  "Martin", "McCreary", "Monroe", "Owsley", "Perry", "Pike", "Powell", "Pulaski",
  "Rockcastle", "Russell", "Wayne", "Whitley", "Wolfe",
]);

/** God's Pantry Food Bank service territory. */
export const GODS_PANTRY_REGION = area([
  "Anderson", "Bath", "Bell", "Bourbon", "Boyle", "Breathitt", "Carter", "Clark", "Clay",
  "Elliott", "Estill", "Fayette", "Fleming", "Floyd", "Franklin", "Garrard", "Harlan",
  "Harrison", "Jackson", "Jessamine", "Johnson", "Knott", "Knox", "Laurel", "Lee",
  "Leslie", "Letcher", "Lewis", "Lincoln", "Madison", "Magoffin", "Martin", "McCreary",
  "Menifee", "Mercer", "Montgomery", "Morgan", "Nicholas", "Owsley", "Perry", "Pike",
  "Powell", "Pulaski", "Robertson", "Rockcastle", "Rowan", "Scott", "Whitley", "Wolfe",
  "Woodford",
]);

/** Feeding America Kentucky's Heartland. */
export const FAKH_REGION = area([
  "Adair", "Allen", "Ballard", "Barren", "Breckinridge", "Butler", "Caldwell", "Calloway",
  "Carlisle", "Casey", "Christian", "Clinton", "Cumberland", "Edmonson", "Fulton", "Graves",
  "Grayson", "Green", "Hancock", "Hardin", "Hart", "Hickman", "LaRue", "Logan", "Lyon",
  "Marion", "Marshall", "McCracken", "Meade", "Metcalfe", "Monroe", "Muhlenberg", "Nelson",
  "Ohio", "Russell", "Simpson", "Taylor", "Todd", "Trigg", "Warren", "Washington", "Wayne",
]);

/** Kentucky Legal Aid western / south-central region (Bowling Green hub). */
export const KLA_WESTERN_REGION = area([
  "Allen", "Barren", "Breckinridge", "Butler", "Caldwell", "Calloway", "Christian",
  "Crittenden", "Daviess", "Edmonson", "Grayson", "Green", "Hancock", "Hardin", "Hart",
  "Henderson", "Hopkins", "LaRue", "Logan", "Lyon", "Marion", "Marshall", "McCracken",
  "McLean", "Meade", "Metcalfe", "Monroe", "Muhlenberg", "Ohio", "Simpson", "Todd", "Trigg",
  "Union", "Warren", "Washington", "Webster",
]);

/** Legal Aid Society — Louisville (Jefferson + surrounding). */
export const LEGAL_AID_LOUISVILLE = area([
  "Anderson", "Bullitt", "Franklin", "Hardin", "Henry", "Jefferson", "LaRue", "Marion",
  "Meade", "Nelson", "Oldham", "Shelby", "Spencer", "Trimble", "Washington",
]);

/** Legal Aid of the Bluegrass. */
export const LEGAL_AID_BLUEGRASS = ADD_REGIONS.bluegrass;

/** KCTCS adult education service areas by college resource ID. */
export const KCTCS_ADULT_ED: Record<string, ServiceArea> = {
  "301": ADD_REGIONS.bluegrass,
  "302": area([
    "Boone", "Bracken", "Campbell", "Carroll", "Grant", "Kenton", "Mason", "Owen",
    "Pendleton", "Robertson",
  ]),
  "303": ADD_REGIONS.barrenRiver,
  "517": area([
    "Boyd", "Carter", "Elliott", "Floyd", "Greenup", "Johnson", "Lawrence", "Magoffin",
    "Martin", "Pike",
  ]),
  "518": ADD_REGIONS.bigSandy,
  "519": ADD_REGIONS.lakeCumberland,
  "520": ADD_REGIONS.greenRiver,
  "521": area([
    "Caldwell", "Christian", "Crittenden", "Hopkins", "Lyon", "Muhlenberg", "Todd", "Trigg",
  ]),
  "522": area([
    "Breathitt", "Harlan", "Knott", "Lee", "Leslie", "Letcher", "Owsley", "Perry", "Wolfe",
  ]),
  "523": ADD_REGIONS.lincolnTrail,
  "524": area([
    "Bath", "Bracken", "Fleming", "Lewis", "Mason", "Menifee", "Montgomery", "Morgan",
    "Robertson", "Rowan",
  ]),
  "525": ADD_REGIONS.pennyrile,
};

/** Per-resource curated overrides (highest priority). */
export const CURATED_BY_ID: Record<string, ServiceArea> = {
  // State agencies / coalitions
  "1": statewide(),
  "2": statewide(),
  "3": statewide(),
  "4": ADD_REGIONS.barrenRiver,
  "5": ADD_REGIONS.fivco,

  // Career centers → workforce regions
  "102": ADD_REGIONS.jefferson,
  "103": ADD_REGIONS.bluegrass,
  "104": ADD_REGIONS.northernKentucky,
  "105": ADD_REGIONS.barrenRiver,
  "106": ADD_REGIONS.fivco,
  "107": EKCEP_REGION,
  "281": EKCEP_REGION,
  "489": ADD_REGIONS.lincolnTrail,
  "492": area(["Anderson", "Franklin", "Owen", "Scott", "Shelby", "Spencer", "Woodford"]),
  "500": ADD_REGIONS.purchase,
  "501": ADD_REGIONS.greenRiver,
  "502": EKCEP_REGION,
  "503": ADD_REGIONS.lakeCumberland,
  "504": ADD_REGIONS.pennyrile,
  "505": ADD_REGIONS.cumberlandValley,

  // CMHC / behavioral health
  "121": ADD_REGIONS.jefferson,
  "123": ADD_REGIONS.bluegrass,
  "124": ADD_REGIONS.northernKentucky,
  "478": area([
    "Bath", "Boyd", "Carter", "Elliott", "Fleming", "Greenup", "Lawrence", "Lewis", "Mason",
    "Menifee", "Montgomery", "Morgan", "Rowan", "Wolfe",
  ]),
  "480": area([
    "Breathitt", "Floyd", "Harlan", "Johnson", "Knott", "Knox", "Lawrence", "Leslie",
    "Letcher", "Magoffin", "Martin", "Morgan", "Perry", "Pike",
  ]),
  "483": ADD_REGIONS.cumberlandValley,
  "488": ADD_REGIONS.lincolnTrail,
  "491": ADD_REGIONS.lincolnTrail,
  "497": area([
    "Allen", "Barren", "Butler", "Edmonson", "Hart", "Logan", "Metcalfe", "Monroe", "Simpson",
    "Warren",
  ]),
  "506": ADD_REGIONS.purchase,
  "507": ADD_REGIONS.greenRiver,
  "508": ADD_REGIONS.lakeCumberland,
  "527": ADD_REGIONS.jefferson,
  "528": ADD_REGIONS.jefferson,
  "529": ADD_REGIONS.jefferson,
  "537": ADD_REGIONS.bluegrass,

  // Legal aid
  "160": LEGAL_AID_LOUISVILLE,
  "161": LEGAL_AID_BLUEGRASS,
  "162": KLA_WESTERN_REGION,
  "163": area([
    ...ADD_REGIONS.greenRiver.counties,
    "Crittenden", "Muhlenberg",
  ]),
  "164": ADD_REGIONS.purchase,
  "165": APPALRED_REGION,
  "482": area([
    "Letcher", "Perry", "Knott", "Harlan", "Pike", "Floyd", "Breathitt", "Leslie", "Lee",
    "Owsley", "Wolfe", "Clay", "Knox", "Bell",
  ]),

  // Food banks
  "181": ADD_REGIONS.jefferson,
  "182": GODS_PANTRY_REGION,
  "183": FAKH_REGION,

  // Community action / ADDs
  "221": ADD_REGIONS.northernKentucky,
  "479": area([
    "Breathitt", "Floyd", "Harlan", "Johnson", "Knott", "Laurel", "Leslie", "Letcher",
    "Magoffin", "Martin", "Perry", "Pike", "Wolfe",
  ]),
  "481": ADD_REGIONS.bigSandy,
  "484": ADD_REGIONS.cumberlandValley,
  "485": ADD_REGIONS.lakeCumberland,
  "494": area([
    "Caldwell", "Christian", "Crittenden", "Hopkins", "Lyon", "Muhlenberg", "Todd", "Trigg",
  ]),
  "495": ADD_REGIONS.greenRiver,
  "511": ADD_REGIONS.pennyrile,
  "512": ADD_REGIONS.purchase,
  "513": ADD_REGIONS.greenRiver,
  "514": ADD_REGIONS.buffaloTrace,
  "515": ADD_REGIONS.barrenRiver,
  "516": KLA_WESTERN_REGION,
  "530": area(["Carroll", "Gallatin", "Grant", "Henry", "Owen", "Trimble"]),
  "533": area(["Boyle", "Garrard"]),
  "534": area(["Lincoln"]),
  "535": area(["Garrard"]),
  "538": area(["Carroll"]),

  // Single-county / local providers (explicit — avoids bad text extraction)
  "10": area(["Jefferson"]),
  "11": area(["Jefferson"]),
  "12": area(["Jefferson"]),
  "13": area(["Jefferson"]),
  "16": area(["Jefferson"]),
  "17": area(["Jefferson"]),
  "18": area(["Jefferson"]),
  "21": area(["Fayette"]),
  "23": area(["Fayette"]),
  "24": area(["Fayette"]),
  "30": area(["Kenton"]),
  "50": area(["Madison"]),
  "51": area(["Madison"]),
  "60": area(["Daviess"]),
  "70": area(["Pike"]),
  "71": area(["McCracken"]),
  "122": area(["Jefferson"]),
  "126": area(["Jefferson"]),
  "127": area(["Jefferson"]),
  "129": area(["Jefferson"]),
  "140": area(["Jefferson"]),
  "141": area(["Jefferson"]),
  "203": area(["Jefferson"]),
  "204": area(["Fayette"]),
  "240": area(["Jefferson"]),
  "241": area(["Fayette"]),
  "261": area(["Jefferson"]),
  "282": area(["Jefferson"]),
  "400": area(["Jefferson"]),
  "402": area(["Fayette"]),
  "403": area(["Fayette"]),
  "406": area(["Jefferson"]),
  "407": area(["Fayette"]),
  "408": area(["Jefferson"]),
  "431": area(["Jefferson"]),
  "432": area(["Jefferson"]),
  "470": area(["Jefferson"]),
  "471": area(["Jefferson"]),
  "473": area(["Jefferson"]),
  "475": ADD_REGIONS.northernKentucky,
  "476": ADD_REGIONS.northernKentucky,
  "477": area(["Campbell", "Kenton"]),
  "531": area(["Boyle"]),
  "536": area(["Estill"]),

  // VOA / metro programs
  "14": ADD_REGIONS.jefferson,
  "15": ADD_REGIONS.jefferson,
  "25": area(["Fayette", "Jessamine", "Scott", "Woodford"]),
  "31": ADD_REGIONS.northernKentucky,
  "41": area(["Warren", "Simpson", "Butler", "Edmonson"]),
  "224": ADD_REGIONS.jefferson,
  "225": area(["Anderson", "Bourbon", "Franklin", "Fayette", "Jessamine", "Scott", "Woodford"]),
  "242": ADD_REGIONS.northernKentucky,
  "401": area(["Jefferson", "Bullitt", "Hardin", "Oldham", "Shelby"]),
  "430": area(["Jefferson"]),
  "474": area(["Jefferson"]),
  "476": area(["Kenton"]),
  "526": area(["Jefferson", "Oldham"]),

  // Drug / specialty courts (county jurisdiction)
  "169": area(["Jefferson"]),
  "170": area(["Jefferson"]),

  // Statewide hotlines / portals (explicit)
  "80": statewide(),
  "100": statewide(),
  "101": statewide(),
  "108": statewide(),
  "109": statewide(),
  "120": statewide(),
  "125": statewide(),
  "128": statewide(),
  "142": statewide(),
  "143": statewide(),
  "166": statewide(),
  "167": statewide(),
  "168": statewide(),
  "171": statewide(),
  "172": statewide(),
  "180": statewide(),
  "184": statewide(),
  "200": statewide(),
  "201": statewide(),
  "202": statewide(),
  "205": statewide(),
  "220": statewide(),
  "222": statewide(),
  "223": statewide(),
  "260": statewide(),
  "262": statewide(),
  "263": statewide(),
  "280": statewide(),
  "283": statewide(),
  "284": statewide(),
  "300": statewide(),
  "304": statewide(),
  "404": statewide(),
  "405": statewide(),
  "409": statewide(),
  "410": statewide(),
  "411": statewide(),
  "412": statewide(),
  "450": statewide(),
  "472": statewide(),
  "20": statewide(),
  "22": statewide(),
  "32": statewide(),
  "40": statewide(),

  // KCTCS adult ed
  ...KCTCS_ADULT_ED,

  // P&P district offices
  ...Object.fromEntries(
    Object.entries(PP_OFFICE_DISTRICT).map(([id, district]) => [
      id,
      PP_DISTRICTS[district],
    ])
  ),
};

/** Name substring → service area for resources not in CURATED_BY_ID. */
export const NAME_PATTERNS: Array<{ test: RegExp; area: ServiceArea }> = [
  { test: /seven counties services/i, area: ADD_REGIONS.jefferson },
  { test: /north key community care/i, area: ADD_REGIONS.northernKentucky },
  { test: /new vista/i, area: ADD_REGIONS.bluegrass },
  { test: /centerstone.*louisville/i, area: area(["Jefferson"]) },
  { test: /dismas charities.*louisville|portland|diersen/i, area: area(["Jefferson"]) },
  { test: /dismas.*lexington/i, area: area(["Fayette"]) },
  { test: /dismas.*owensboro/i, area: area(["Daviess"]) },
  { test: /social security.*louisville/i, area: area(["Jefferson"]) },
  { test: /social security.*lexington/i, area: area(["Fayette"]) },
  { test: /probation & parole|probation and parole/i, area: area([]) }, // handled by PP_OFFICE_DISTRICT
  { test: /kentucky career center/i, area: area([]) }, // handled by CURATED
  { test: /kctcs.*adult education/i, area: area([]) },
];
