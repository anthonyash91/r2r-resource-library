/**
 * Populate served_counties and coverage on data/resources.csv for all resources.
 *
 * Usage:
 *   npx tsx scripts/migrate-served-counties.ts
 *   npm run seed:resources
 */
import { readFileSync, writeFileSync } from "fs";
import { resolve } from "path";
import {
  KENTUCKY_COUNTIES,
  normalizeCountyName,
} from "../src/lib/kentucky/counties";
import {
  CURATED_BY_ID,
  NAME_PATTERNS,
  PP_OFFICE_DISTRICT,
  PP_DISTRICTS,
  type Coverage,
  type ServiceArea,
} from "./lib/kentucky-service-areas";

const CSV_PATH = resolve(process.cwd(), "data/resources.csv");

const COLUMNS = [
  "id",
  "name",
  "category",
  "region",
  "description",
  "description_es",
  "address",
  "city",
  "phone",
  "email",
  "website",
  "eligibility",
  "eligibility_es",
  "notes",
  "notes_es",
  "hours",
  "tags",
  "services",
  "county",
  "latitude",
  "longitude",
  "served_counties",
  "coverage",
] as const;

const STATEWIDE_TAG = /\bstatewide\b/i;
const STATEWIDE_REGION = /^statewide$/i;
const STATEWIDE_TEXT =
  /\ball 120 counties\b|\b120 counties\b|\bstatewide\b|\btodo el estado\b|\ben todo el estado\b|\bacross kentucky\b|\bthroughout kentucky\b|\bentire state\b|\bwhole state\b|\bstate of kentucky\b/i;

/** Explicit county list patterns in descriptions. */
const COUNTY_LIST_PATTERNS = [
  /(?:serves?|serving|serve|atend(?:e|iendo)?)\s+(?:the\s+)?(\d+)\s+[\w-]+\s+count(?:y|ies)[:\s]+([^.]+?)(?:\.|$)/i,
  /(?:counties|condados)[:\s]+([^.]+?)(?:\.|$)/i,
  /(?:including|including the counties of|in)\s+([A-Z][a-z]+(?:,\s+[A-Z][a-z]+){2,})/,
];

function parseCsv(content: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let inQuotes = false;

  for (let i = 0; i < content.length; i++) {
    const char = content[i];
    const next = content[i + 1];

    if (inQuotes) {
      if (char === '"' && next === '"') {
        field += '"';
        i++;
      } else if (char === '"') {
        inQuotes = false;
      } else {
        field += char;
      }
      continue;
    }

    if (char === '"') {
      inQuotes = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n" || (char === "\r" && next === "\n")) {
      row.push(field);
      if (row.some((cell) => cell.trim())) rows.push(row);
      row = [];
      field = "";
      if (char === "\r") i++;
    } else if (char !== "\r") {
      field += char;
    }
  }

  if (field.length > 0 || row.length > 0) {
    row.push(field);
    if (row.some((cell) => cell.trim())) rows.push(row);
  }

  return rows;
}

function escapeCsvField(value: string) {
  if (/[",\n\r]/.test(value)) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

function serializeCsv(rows: string[][]) {
  return rows.map((row) => row.map(escapeCsvField).join(",")).join("\n") + "\n";
}

function extractCountiesFromText(...parts: string[]): string[] {
  const combined = parts.filter(Boolean).join(" ");
  const found = new Set<string>();

  for (const county of KENTUCKY_COUNTIES) {
    const pattern = new RegExp(`\\b${county.replace(/'/g, "''")}\\b`, "i");
    if (pattern.test(combined)) {
      found.add(county);
    }
  }

  if (/\bLa\s?Rue\b/i.test(combined)) found.add("LaRue");

  for (const pattern of COUNTY_LIST_PATTERNS) {
    const match = combined.match(pattern);
    if (match?.[1]) {
      const segment = match[match.length - 1];
      for (const county of KENTUCKY_COUNTIES) {
        if (new RegExp(`\\b${county}\\b`, "i").test(segment)) {
          found.add(county);
        }
      }
    }
  }

  return [...found].sort((a, b) => a.localeCompare(b));
}

function toResult(area: ServiceArea): { coverage: Coverage; counties: string[] } {
  return { coverage: area.coverage, counties: area.counties };
}

function inferCoverage(record: Record<string, string>): {
  coverage: Coverage;
  counties: string[];
} {
  const id = record.id?.trim() ?? "";
  const name = record.name ?? "";

  if (id && CURATED_BY_ID[id]) {
    return toResult(CURATED_BY_ID[id]);
  }

  if (id && PP_OFFICE_DISTRICT[id]) {
    return toResult(PP_DISTRICTS[PP_OFFICE_DISTRICT[id]]);
  }

  for (const { test, area } of NAME_PATTERNS) {
    if (test.test(name) && area.counties.length > 0) {
      return toResult(area);
    }
  }

  const region = record.region?.trim() ?? "";
  const tags = record.tags ?? "";
  const blob = [
    record.description,
    record.description_es,
    record.notes,
    record.notes_es,
    record.eligibility,
    record.name,
    region,
  ]
    .filter(Boolean)
    .join(" ");

  if (
    STATEWIDE_REGION.test(region) ||
    STATEWIDE_TAG.test(tags) ||
    STATEWIDE_TEXT.test(blob)
  ) {
    return { coverage: "statewide", counties: [] };
  }

  const extracted = extractCountiesFromText(
    record.description ?? "",
    record.description_es ?? "",
    record.notes ?? "",
    record.notes_es ?? "",
    record.eligibility ?? "",
    record.eligibility_es ?? "",
    record.name ?? "",
    record.region ?? ""
  );

  const primary = normalizeCountyName(record.county ?? "");
  if (primary && !extracted.includes(primary)) {
    extracted.unshift(primary);
  }

  const unique = [...new Set(extracted)];

  if (unique.length >= 2) {
    return { coverage: "multi", counties: unique };
  }

  if (unique.length === 1) {
    return { coverage: "single", counties: unique };
  }

  if (primary) {
    return { coverage: "single", counties: [primary] };
  }

  return { coverage: "single", counties: [] };
}

const raw = readFileSync(CSV_PATH, "utf8");
const rows = parseCsv(raw);
const oldHeader = rows[0].map((h) => h.trim().toLowerCase());

const records = rows.slice(1).map((values) => {
  const record: Record<string, string> = {};
  oldHeader.forEach((key, index) => {
    record[key] = values[index] ?? "";
  });
  return record;
});

let statewide = 0;
let multi = 0;
let single = 0;
let curated = 0;
let extracted = 0;

for (const record of records) {
  const id = record.id?.trim() ?? "";
  const before = `${record.coverage}|${record.served_counties}`;
  const { coverage, counties } = inferCoverage(record);
  record.served_counties = counties.join("|");
  record.coverage = coverage;

  if (id && CURATED_BY_ID[id]) curated++;
  else if (counties.length >= 2) extracted++;

  if (coverage === "statewide") statewide++;
  else if (coverage === "multi") multi++;
  else single++;

  void before;
}

const outRows: string[][] = [Array.from(COLUMNS)];
for (const record of records) {
  outRows.push(COLUMNS.map((col) => record[col] ?? ""));
}

writeFileSync(CSV_PATH, serializeCsv(outRows));

console.log(`Updated ${records.length} resources in ${CSV_PATH}`);
console.log(`  coverage: ${single} single, ${multi} multi, ${statewide} statewide`);
console.log(`  curated by ID: ${curated}, multi from text/heuristics: ${extracted}`);
console.log(
  `  with served_counties: ${records.filter((r) => r.served_counties?.trim()).length}/${records.length}`
);
console.log(
  `  non-statewide missing counties: ${records.filter((r) => r.coverage !== "statewide" && !r.served_counties?.trim()).length}`
);
console.log("\nNext: npm run seed:resources → run migration 005 + seed-resources.sql");
