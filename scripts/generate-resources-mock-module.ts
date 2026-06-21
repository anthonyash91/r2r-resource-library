/**
 * Generates src/lib/{state-slug}/resources.generated.ts from a resources CSV.
 *
 * Usage:
 *   npx tsx scripts/generate-resources-mock-module.ts data/ohio-resources.csv Ohio oh
 */
import { readFileSync, writeFileSync } from "fs";
import { resolve } from "path";
import { KENTUCKY_CATEGORIES } from "../src/lib/kentucky/categories";
import { isValidCoverage } from "../src/lib/resource-coverage";

const INPUT = process.argv[2];
const STATE = process.argv[3] ?? "Ohio";
const ID_PREFIX = process.argv[4] ?? "oh";

if (!INPUT) {
  console.error("Usage: npx tsx scripts/generate-resources-mock-module.ts <csv-path> [StateName] [id-prefix]");
  process.exit(1);
}

const CATEGORY_ID_BY_SLUG = Object.fromEntries(
  KENTUCKY_CATEGORIES.map((c) => [c.slug, c.id])
);

const CATEGORY_ALIASES: Record<string, string> = {
  "state-agency": "state-agency",
  housing: "housing",
  employment: "employment",
  healthcare: "healthcare",
  "substance-use-treatment": "substance-use-treatment",
  "legal-aid": "legal-aid",
  "food-nutrition": "food-nutrition",
  "id-documentation": "id-documentation",
  "financial-assistance": "financial-assistance",
  transportation: "transportation",
  "family-children": "family-children",
  "peer-support": "peer-support",
  education: "education",
  veterans: "veterans",
  "basic-needs": "basic-needs",
  "probation-parole": "probation-parole",
  "reentry-organizations": "reentry-organizations",
};

function normalizeKey(value: string) {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

function resolveCategorySlug(raw: string): string | null {
  const key = normalizeKey(raw);
  if (!key) return null;
  if (CATEGORY_ID_BY_SLUG[key]) return key;
  const alias = CATEGORY_ALIASES[key];
  if (alias) return alias;
  const bySlug = KENTUCKY_CATEGORIES.find((c) => normalizeKey(c.slug) === key);
  if (bySlug) return bySlug.slug;
  const byName = KENTUCKY_CATEGORIES.find((c) => normalizeKey(c.name) === key);
  return byName?.slug ?? null;
}

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

function cell(row: Record<string, string>, key: string) {
  return (row[key] ?? "").trim();
}

function parseListField(value: string) {
  if (!value.trim()) return [];
  return value
    .split(/[|,]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function parseCoordinate(value: string) {
  if (!value.trim()) return null;
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
}

function tsString(value: string | null | undefined) {
  if (value === null || value === undefined || !value.trim()) return "null";
  return JSON.stringify(value);
}

function tsArray(values: string[]) {
  if (!values.length) return "[]";
  return `[${values.map((v) => JSON.stringify(v)).join(", ")}]`;
}

const inputPath = resolve(process.cwd(), INPUT);
const raw = readFileSync(inputPath, "utf8");
const rows = parseCsv(raw);

if (rows.length < 2) {
  console.error(`No data rows in ${INPUT}`);
  process.exit(1);
}

const headers = rows[0].map((h) => normalizeKey(h));
const records = rows.slice(1).map((values) => {
  const record: Record<string, string> = {};
  headers.forEach((header, index) => {
    record[header] = values[index] ?? "";
  });
  return record;
});

const errors: string[] = [];
const seeds = records.map((row, index) => {
  const sourceId = cell(row, "id") || String(index + 1);
  const name = cell(row, "name");
  const categorySlug = resolveCategorySlug(cell(row, "category"));

  if (!name) errors.push(`Row ${index + 2}: missing name`);
  if (!categorySlug) errors.push(`Row ${index + 2}: unknown category "${cell(row, "category")}"`);

  const coverageRaw = cell(row, "coverage") || "single";
  const coverage = isValidCoverage(coverageRaw) ? coverageRaw : "single";

  return {
    id: `res-${ID_PREFIX}-${String(index + 1).padStart(3, "0")}`,
    name,
    description: cell(row, "description"),
    description_es: cell(row, "description_es") || null,
    category_id: categorySlug ? CATEGORY_ID_BY_SLUG[categorySlug] : "cat-ky-reentry-orgs",
    state: STATE,
    county: cell(row, "county") || null,
    city: cell(row, "city") || null,
    address: cell(row, "address") || null,
    phone: cell(row, "phone") || null,
    website: cell(row, "website") || null,
    email: cell(row, "email") || null,
    hours: cell(row, "hours") || null,
    eligibility: cell(row, "eligibility") || null,
    eligibility_es: cell(row, "eligibility_es") || null,
    notes: cell(row, "notes") || null,
    notes_es: cell(row, "notes_es") || null,
    served_counties: parseListField(cell(row, "served_counties")),
    coverage,
    services: parseListField(cell(row, "services")),
    tags: parseListField(cell(row, "tags")),
    latitude: parseCoordinate(cell(row, "latitude")),
    longitude: parseCoordinate(cell(row, "longitude")),
    sourceId,
  };
});

if (errors.length) {
  console.error("Cannot generate mock module:\n", errors.join("\n"));
  process.exit(1);
}

const slug = STATE.toLowerCase().replace(/\s+/g, "-");
const outputPath = resolve(process.cwd(), `src/lib/${slug}/resources.generated.ts`);

const seedBlocks = seeds
  .map(
    (s) => `  {
    id: ${tsString(s.id)},
    name: ${tsString(s.name)},
    description: ${tsString(s.description)},
    description_es: ${tsString(s.description_es)},
    category_id: ${tsString(s.category_id)},
    state: ${tsString(s.state)},
    county: ${tsString(s.county)},
    city: ${tsString(s.city)},
    address: ${tsString(s.address)},
    phone: ${tsString(s.phone)},
    website: ${tsString(s.website)},
    email: ${tsString(s.email)},
    hours: ${tsString(s.hours)},
    eligibility: ${tsString(s.eligibility)},
    eligibility_es: ${tsString(s.eligibility_es)},
    notes: ${tsString(s.notes)},
    notes_es: ${tsString(s.notes_es)},
    served_counties: ${tsArray(s.served_counties)},
    coverage: ${tsString(s.coverage)},
    services: ${tsArray(s.services)},
    tags: ${tsArray(s.tags)},
    latitude: ${s.latitude ?? "null"},
    longitude: ${s.longitude ?? "null"},
  }`
  )
  .join(",\n");

const content = `/* eslint-disable */
/** Auto-generated from ${INPUT} — do not edit by hand. Regenerate: npm run seed:resources:ohio */
import type { Resource } from "@/types";
import { KENTUCKY_CATEGORY_BY_ID } from "@/lib/kentucky/categories";

const now = new Date().toISOString();

type ResourceSeed = Omit<
  Resource,
  | "category"
  | "created_at"
  | "updated_at"
  | "view_count"
  | "save_count"
  | "status"
  | "created_by"
  | "is_featured"
>;

function buildResource(seed: ResourceSeed): Resource {
  return {
    ...seed,
    category: KENTUCKY_CATEGORY_BY_ID[seed.category_id],
    status: "active",
    is_featured: false,
    view_count: 0,
    save_count: 0,
    created_at: now,
    updated_at: now,
    created_by: null,
  };
}

const RESOURCE_SEEDS: ResourceSeed[] = [
${seedBlocks}
];

export const OHIO_RESOURCES: Resource[] = RESOURCE_SEEDS.map(buildResource);
`;

writeFileSync(outputPath, content);
console.log(`Wrote ${outputPath} (${seeds.length} resources)`);
