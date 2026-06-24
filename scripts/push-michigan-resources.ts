/**
 * Upsert Michigan resources from data/michigan-resources.csv into Supabase.
 * Requires SUPABASE_SERVICE_ROLE_KEY in .env.local (admin RLS bypass).
 *
 * Usage: npm run db:push:michigan
 */
import { readFileSync, existsSync } from "fs";
import { resolve } from "path";
import { createClient } from "@supabase/supabase-js";
import { KENTUCKY_CATEGORIES } from "../src/lib/kentucky/categories";
import { isValidCoverage } from "../src/lib/resource-coverage";

function loadEnvLocal() {
  const path = resolve(process.cwd(), ".env.local");
  if (!existsSync(path)) return;
  for (const line of readFileSync(path, "utf8").split("\n")) {
    const match = line.match(/^([^#=]+)=(.*)$/);
    if (match && !process.env[match[1].trim()]) {
      process.env[match[1].trim()] = match[2].trim().replace(/^"|"$/g, "");
    }
  }
}

loadEnvLocal();

const CSV_PATH = resolve(process.cwd(), "data/michigan-resources.csv");
const UUID_PREFIX = "d5000001";
const BATCH_SIZE = 50;

const CATEGORY_UUID = Object.fromEntries(
  KENTUCKY_CATEGORIES.map((category, index) => [
    category.slug,
    `c1000001-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`,
  ])
);

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
      } else if (char === '"') inQuotes = false;
      else field += char;
      continue;
    }
    if (char === '"') inQuotes = true;
    else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n" || (char === "\r" && next === "\n")) {
      row.push(field);
      if (row.some((c) => c.trim())) rows.push(row);
      row = [];
      field = "";
      if (char === "\r") i++;
    } else if (char !== "\r") field += char;
  }
  if (field.length || row.length) {
    row.push(field);
    if (row.some((c) => c.trim())) rows.push(row);
  }
  return rows;
}

function cell(row: Record<string, string>, key: string) {
  return (row[key] ?? "").trim();
}

function parseList(value: string) {
  if (!value.trim()) return [];
  return value
    .split(/[|,]/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function resourceUuid(index: number) {
  return `${UUID_PREFIX}-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`;
}

async function main() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !serviceKey) {
    console.error(
      "Missing NEXT_PUBLIC_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY.\n" +
        "Add SUPABASE_SERVICE_ROLE_KEY to .env.local, or run supabase/seed-michigan-resources.sql in the SQL Editor."
    );
    process.exit(1);
  }

  const raw = readFileSync(CSV_PATH, "utf8");
  const rows = parseCsv(raw);
  const headers = rows[0].map((h) => h.trim().toLowerCase());
  const records = rows.slice(1).map((values) => {
    const record: Record<string, string> = {};
    headers.forEach((h, i) => {
      record[h] = values[i] ?? "";
    });
    return record;
  });

  const supabase = createClient(url, serviceKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  const payloads = records.map((row, index) => {
    const slug = cell(row, "category");
    const categoryId = CATEGORY_UUID[slug];
    if (!categoryId) throw new Error(`Unknown category "${slug}" on row ${index + 2}`);
    const coverageRaw = cell(row, "coverage") || "single";
    return {
      id: resourceUuid(index),
      name: cell(row, "name"),
      description: cell(row, "description"),
      description_es: cell(row, "description_es") || null,
      category_id: categoryId,
      state: "Michigan",
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
      served_counties: parseList(cell(row, "served_counties")),
      coverage: isValidCoverage(coverageRaw) ? coverageRaw : "single",
      services: parseList(cell(row, "services")),
      tags: parseList(cell(row, "tags")),
      intake_signals: parseList(cell(row, "intake_signals")),
      is_featured: false,
      status: "active" as const,
    };
  });

  let upserted = 0;
  for (let i = 0; i < payloads.length; i += BATCH_SIZE) {
    const batch = payloads.slice(i, i + BATCH_SIZE);
    const { error } = await supabase.from("resources").upsert(batch, { onConflict: "id" });
    if (error) {
      console.error(`Batch ${i / BATCH_SIZE + 1} failed:`, error.message);
      process.exit(1);
    }
    upserted += batch.length;
    console.log(`Upserted ${upserted}/${payloads.length}`);
  }

  const { count } = await supabase
    .from("resources")
    .select("*", { count: "exact", head: true })
    .eq("state", "Michigan");
  console.log(`Done. Michigan resources in database: ${count ?? upserted}`);
}

main();
