/**
 * Generates supabase/seed-resources.sql from a CSV file.
 *
 * Expected columns (header row):
 *   id,name,category,region,description,description_es,address,city,phone,email,website,eligibility,eligibility_es,notes,notes_es,hours,tags,services,county,latitude,longitude
 *
 * Column mapping:
 *   id            → stable UUID (row order); your id is kept in SQL comments for reference
 *   name          → resources.name (required)
 *   category      → resources.category_id (matched by Kentucky category name or slug)
 *   region        → resources.county (area/region label)
 *   description   → resources.description (required)
 *   description_es→ resources.description_es
 *   address       → resources.address
 *   city          → resources.city
 *   phone         → resources.phone
 *   email         → resources.email
 *   website       → resources.website
 *   eligibility   → resources.eligibility (who qualifies — not operational tips)
 *   eligibility_es→ resources.eligibility_es
 *   notes         → resources.notes (operational tips: crisis lines, alternate locations, etc.)
 *   notes_es      → resources.notes_es
 *   hours         → resources.hours (optional)
 *   tags          → resources.tags — comma- or pipe-separated (optional)
 *   services      → resources.services — comma- or pipe-separated (optional)
 *   county        → resources.county — primary office county (optional)
 *   latitude      → resources.latitude (optional)
 *   longitude     → resources.longitude (optional)
 *   served_counties → resources.served_counties — pipe-separated KY county names
 *   coverage      → resources.coverage — single | multi | statewide
 *
 * Defaults for columns not in CSV:
 *   state         → Kentucky (override with RESOURCES_DEFAULT_STATE env var)
 *   is_featured   → false
 *   status        → active
 *
 * Usage:
 *   npx tsx scripts/generate-resources-seed.ts data/resources.csv
 *   npx tsx scripts/generate-resources-seed.ts path/to/your-export.csv
 *
 * Then run supabase/seed-resources.sql in the Supabase SQL Editor after migrations.
 */
import { readFileSync, writeFileSync } from "fs";
import { resolve } from "path";
import { KENTUCKY_CATEGORIES } from "../src/lib/kentucky/categories";
import { isValidCoverage } from "../src/lib/resource-coverage";

const DEFAULT_STATE = process.env.RESOURCES_DEFAULT_STATE ?? "Kentucky";
const INPUT = process.argv[2] ?? "data/resources.csv";
const OUTPUT = process.env.RESOURCES_SEED_OUTPUT ?? "supabase/seed-resources.sql";
const UUID_PREFIX = process.env.RESOURCES_UUID_PREFIX ?? "d1000001";
const INCLUDE_CATEGORIES = process.env.RESOURCES_INCLUDE_CATEGORIES !== "false";

const CATEGORY_UUID = Object.fromEntries(
  KENTUCKY_CATEGORIES.map((category, index) => [
    category.slug,
    `c1000001-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`,
  ])
);

const CATEGORY_ALIASES: Record<string, string> = {
  "state agency": "state-agency",
  housing: "housing",
  employment: "employment",
  healthcare: "healthcare",
  "health care": "healthcare",
  "mental health": "healthcare",
  "substance use": "substance-use-treatment",
  "substance use treatment": "substance-use-treatment",
  recovery: "substance-use-treatment",
  "legal aid": "legal-aid",
  legal: "legal-aid",
  "food & nutrition": "food-nutrition",
  "food assistance": "food-nutrition",
  food: "food-nutrition",
  "id & documentation": "id-documentation",
  identification: "id-documentation",
  ids: "id-documentation",
  "financial assistance": "financial-assistance",
  financial: "financial-assistance",
  transportation: "transportation",
  transit: "transportation",
  "family & children": "family-children",
  family: "family-children",
  "peer support": "peer-support",
  education: "education",
  veterans: "veterans",
  "basic needs": "basic-needs",
  "probation & parole": "probation-parole",
  probation: "probation-parole",
  parole: "probation-parole",
  "reentry organizations": "reentry-organizations",
  reentry: "reentry-organizations",
  nonprofit: "reentry-organizations",
};

function normalizeKey(value: string) {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

function resolveCategorySlug(raw: string): string | null {
  const key = normalizeKey(raw);
  if (!key) return null;

  if (CATEGORY_UUID[key]) return key;

  const alias = CATEGORY_ALIASES[key];
  if (alias) return alias;

  const bySlug = KENTUCKY_CATEGORIES.find((c) => normalizeKey(c.slug) === key);
  if (bySlug) return bySlug.slug;

  const byName = KENTUCKY_CATEGORIES.find((c) => normalizeKey(c.name) === key);
  if (byName) return byName.slug;

  const byPartial = KENTUCKY_CATEGORIES.find(
    (c) => key.includes(normalizeKey(c.name)) || normalizeKey(c.name).includes(key)
  );
  return byPartial?.slug ?? null;
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

function sqlString(value: string | null | undefined) {
  if (value === null || value === undefined) return "NULL";
  const trimmed = value.trim();
  if (!trimmed) return "NULL";
  return `'${trimmed.replace(/'/g, "''")}'`;
}

function sqlArray(values: string[]) {
  if (!values.length) return "ARRAY[]::TEXT[]";
  return `ARRAY[${values.map((v) => sqlString(v)).join(", ")}]`;
}

function resourceUuid(index: number) {
  return `${UUID_PREFIX}-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`;
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

const OPTIONAL_FIELDS = [
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

const inputPath = resolve(process.cwd(), INPUT);
const raw = readFileSync(inputPath, "utf8");
const rows = parseCsv(raw);

if (rows.length < 2) {
  console.error(`No data rows found in ${INPUT}. Add rows below the header.`);
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
const warnings: string[] = [];
const unknownCategories = new Set<string>();

const resourceInserts = records
  .map((row, index) => {
    const sourceId = cell(row, "id") || String(index + 1);
    const name = cell(row, "name");
    const description = cell(row, "description");
    const categoryRaw = cell(row, "category");
    const categorySlug = resolveCategorySlug(categoryRaw);

    if (!name) errors.push(`Row ${index + 2} (${sourceId}): missing name`);
    if (!description) errors.push(`Row ${index + 2} (${sourceId}): missing description`);
    if (!categorySlug) {
      unknownCategories.add(categoryRaw || "(empty)");
      errors.push(`Row ${index + 2} (${sourceId}): unknown category "${categoryRaw}"`);
    }

    const descriptionEs = cell(row, "description_es") || null;

    const uuid = resourceUuid(index);
    const county = cell(row, "county") || cell(row, "region") || null;
    const latitude = parseCoordinate(cell(row, "latitude"));
    const longitude = parseCoordinate(cell(row, "longitude"));
    const services = parseListField(cell(row, "services"));
    const tags = parseListField(cell(row, "tags"));
    const servedCounties = parseListField(cell(row, "served_counties"));
    const coverageRaw = cell(row, "coverage") || "single";
    const coverage = isValidCoverage(coverageRaw) ? coverageRaw : "single";
    if (cell(row, "coverage") && !isValidCoverage(coverageRaw)) {
      warnings.push(`Row ${index + 2} (${sourceId}): invalid coverage "${coverageRaw}", using single`);
    }

    if (cell(row, "latitude") && latitude === null) {
      warnings.push(`Row ${index + 2} (${sourceId}): invalid latitude`);
    }
    if (cell(row, "longitude") && longitude === null) {
      warnings.push(`Row ${index + 2} (${sourceId}): invalid longitude`);
    }

    return `  -- source id: ${sourceId.replace(/\n/g, " ")}
  (
    ${sqlString(uuid)},
    ${sqlString(name)},
    ${sqlString(description)},
    ${sqlString(descriptionEs || null)},
    ${sqlString(categorySlug ? CATEGORY_UUID[categorySlug] : null)},
    ${sqlString(DEFAULT_STATE)},
    ${sqlString(county)},
    ${sqlString(cell(row, "city") || null)},
    ${sqlString(cell(row, "address") || null)},
    ${sqlString(cell(row, "phone") || null)},
    ${sqlString(cell(row, "website") || null)},
    ${sqlString(cell(row, "email") || null)},
    ${sqlString(cell(row, "hours") || null)},
    ${sqlString(cell(row, "eligibility") || null)},
    ${sqlString(cell(row, "eligibility_es") || null)},
    ${sqlString(cell(row, "notes") || null)},
    ${sqlString(cell(row, "notes_es") || null)},
    ${sqlArray(servedCounties)},
    ${sqlString(coverage)},
    ${sqlArray(services)},
    ${sqlArray(tags)},
    ${latitude ?? "NULL"},
    ${longitude ?? "NULL"},
    false,
    'active'
  )`;
  })
  .join(",\n");

if (errors.length) {
  console.error("\nCannot generate seed — fix these issues first:\n");
  errors.forEach((e) => console.error(`  • ${e}`));
  if (unknownCategories.size) {
    console.error("\nKnown category names:");
    KENTUCKY_CATEGORIES.forEach((c) => console.error(`  • ${c.name} (${c.slug})`));
  }
  process.exit(1);
}

const categoryList = KENTUCKY_CATEGORIES.map(
  (c) =>
    `  (${sqlString(CATEGORY_UUID[c.slug])}, ${sqlString(c.name)}, ${sqlString(c.slug)}, ${sqlString(c.description)}, ${sqlString(c.icon)}, ${c.sort_order}, ${c.is_active})`
).join(",\n");

const categoriesSql = INCLUDE_CATEGORIES
  ? `INSERT INTO categories (id, name, slug, description, icon, sort_order, is_active) VALUES
${categoryList}
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  icon = EXCLUDED.icon,
  sort_order = EXCLUDED.sort_order,
  is_active = EXCLUDED.is_active;

`
  : `-- Categories skipped (RESOURCES_INCLUDE_CATEGORIES=false); run Kentucky seed first.

`;

const sql = `-- Resource import seed (generated from CSV)
-- Source file: ${INPUT}
-- State: ${DEFAULT_STATE}
-- UUID prefix: ${UUID_PREFIX}
-- Generated: ${new Date().toISOString()}
-- Run after: supabase/migrations/001_initial_schema.sql
--            supabase/migrations/002_add_description_es.sql
--            supabase/migrations/004_add_eligibility_es_and_notes.sql
--            supabase/migrations/005_add_served_counties.sql
-- Regenerate: RESOURCES_DEFAULT_STATE="${DEFAULT_STATE}" RESOURCES_UUID_PREFIX="${UUID_PREFIX}" RESOURCES_SEED_OUTPUT="${OUTPUT}" npx tsx scripts/generate-resources-seed.ts ${INPUT}

${categoriesSql}INSERT INTO resources (
  id, name, description, description_es, category_id,
  state, county, city, address, phone, website, email, hours,
  eligibility, eligibility_es, notes, notes_es,
  served_counties, coverage,
  services, tags, latitude, longitude, is_featured, status
) VALUES
${resourceInserts}
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  description_es = EXCLUDED.description_es,
  category_id = EXCLUDED.category_id,
  state = EXCLUDED.state,
  county = EXCLUDED.county,
  city = EXCLUDED.city,
  address = EXCLUDED.address,
  phone = EXCLUDED.phone,
  website = EXCLUDED.website,
  email = EXCLUDED.email,
  hours = EXCLUDED.hours,
  eligibility = EXCLUDED.eligibility,
  eligibility_es = EXCLUDED.eligibility_es,
  notes = EXCLUDED.notes,
  notes_es = EXCLUDED.notes_es,
  served_counties = EXCLUDED.served_counties,
  coverage = EXCLUDED.coverage,
  services = EXCLUDED.services,
  tags = EXCLUDED.tags,
  latitude = EXCLUDED.latitude,
  longitude = EXCLUDED.longitude,
  is_featured = EXCLUDED.is_featured,
  status = EXCLUDED.status,
  updated_at = NOW();
`;

writeFileSync(OUTPUT, sql);
console.log(`Wrote ${OUTPUT} (${records.length} resources from ${INPUT})`);

const gapRows = records
  .map((row, index) => {
    const missing = OPTIONAL_FIELDS.filter((field) => !cell(row, field));
    if (!missing.length) return null;
    const sourceId = cell(row, "id") || String(index + 1);
    const label = cell(row, "name") || sourceId;
    return { sourceId, label, missing };
  })
  .filter(
    (row): row is { sourceId: string; label: string; missing: (typeof OPTIONAL_FIELDS)[number][] } =>
      row !== null
  );

if (gapRows.length) {
  console.log(`\n${gapRows.length} row(s) still have empty optional fields:`);
  gapRows.forEach(({ sourceId, label, missing }) => {
    console.log(`  • id ${sourceId} — ${label}`);
    console.log(`    missing: ${missing.join(", ")}`);
  });
  console.log("\nTip: add hours, tags, services, county, latitude, longitude columns to the CSV.");
}

if (warnings.length) {
  console.log("\nWarnings:");
  warnings.forEach((w) => console.log(`  • ${w}`));
}
console.log("\nNext: run supabase/seed-resources.sql in the Supabase SQL Editor.");
