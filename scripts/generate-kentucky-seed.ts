/**
 * Generates supabase/seed-kentucky.sql from TypeScript source data.
 * Run: npx tsx scripts/generate-kentucky-seed.ts
 */
import { writeFileSync } from "fs";
import { KENTUCKY_CATEGORIES } from "../src/lib/kentucky/categories";
import { KENTUCKY_RESOURCES } from "../src/lib/kentucky/resources";

const CATEGORY_UUID = Object.fromEntries(
  KENTUCKY_CATEGORIES.map((category, index) => [
    category.id,
    `c1000001-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`,
  ])
);

const RESOURCE_UUID = Object.fromEntries(
  KENTUCKY_RESOURCES.map((resource, index) => [
    resource.id,
    `b1000001-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`,
  ])
);

function sqlString(value: string | null | undefined) {
  if (value === null || value === undefined) return "NULL";
  return `'${String(value).replace(/'/g, "''")}'`;
}

function sqlArray(values: string[]) {
  if (!values.length) return "ARRAY[]::TEXT[]";
  return `ARRAY[${values.map((v) => sqlString(v)).join(", ")}]`;
}

const categoryInserts = KENTUCKY_CATEGORIES.map(
  (c) =>
    `  (${sqlString(CATEGORY_UUID[c.id])}, ${sqlString(c.name)}, ${sqlString(c.slug)}, ${sqlString(c.description)}, ${sqlString(c.icon)}, ${c.sort_order}, ${c.is_active})`
).join(",\n");

const resourceInserts = KENTUCKY_RESOURCES.map((r) => {
  return `  (
    ${sqlString(RESOURCE_UUID[r.id])},
    ${sqlString(r.name)},
    ${sqlString(r.description)},
    ${sqlString(r.description_es ?? null)},
    ${sqlString(CATEGORY_UUID[r.category_id])},
    ${sqlString(r.state)},
    ${sqlString(r.county)},
    ${sqlString(r.city)},
    ${sqlString(r.address)},
    ${sqlString(r.phone)},
    ${sqlString(r.website)},
    ${sqlString(r.email)},
    ${sqlString(r.hours)},
    ${sqlString(r.eligibility)},
    ${sqlArray(r.services)},
    ${sqlArray(r.tags)},
    ${r.is_featured},
    ${sqlString(r.status)}
  )`;
}).join(",\n");

const sql = `-- Kentucky reentry resources for Reentry to Recovery
-- Generated from src/lib/kentucky/*.ts
-- Run after: supabase/migrations/001_initial_schema.sql
--            supabase/migrations/002_add_description_es.sql
-- Optional reset first: supabase/reset-data.sql
-- Regenerate: npx tsx scripts/generate-kentucky-seed.ts

INSERT INTO categories (id, name, slug, description, icon, sort_order, is_active) VALUES
${categoryInserts}
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  icon = EXCLUDED.icon,
  sort_order = EXCLUDED.sort_order,
  is_active = EXCLUDED.is_active;

INSERT INTO resources (
  id, name, description, description_es, category_id,
  state, county, city, address, phone, website, email, hours, eligibility,
  services, tags, is_featured, status
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
  services = EXCLUDED.services,
  tags = EXCLUDED.tags,
  is_featured = EXCLUDED.is_featured,
  status = EXCLUDED.status,
  updated_at = NOW();
`;

writeFileSync("supabase/seed-kentucky.sql", sql);
console.log(`Wrote supabase/seed-kentucky.sql (${KENTUCKY_RESOURCES.length} resources)`);
