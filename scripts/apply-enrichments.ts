/**
 * Merge enrichment JSON into a resources CSV by resource id.
 *
 * Usage:
 *   npx tsx scripts/apply-enrichments.ts data/enrichments/batch-01.json
 *   npx tsx scripts/apply-enrichments.ts data/enrichments/ohio-enriched.json data/ohio-resources.csv
 *   npm run seed:resources
 */
import { readFileSync, writeFileSync } from "fs";
import { resolve } from "path";

const CSV_PATH = resolve(process.cwd(), process.argv[3] ?? "data/resources.csv");
const ENRICHMENT_PATH = resolve(process.cwd(), process.argv[2] ?? "data/enrichments/batch-01.json");

const ALL_COLUMNS = [
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
  "served_counties",
  "coverage",
] as const;

type Column = (typeof ALL_COLUMNS)[number];

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

const enrichments = JSON.parse(readFileSync(ENRICHMENT_PATH, "utf8")) as Record<
  string,
  Partial<Record<Column, string>>
>;

const raw = readFileSync(CSV_PATH, "utf8");
const rows = parseCsv(raw);
const header = rows[0].map((h) => h.trim().toLowerCase());

for (const col of ALL_COLUMNS) {
  if (!header.includes(col)) header.push(col);
}

const records = rows.slice(1).map((values) => {
  const record: Record<string, string> = {};
  rows[0].forEach((key, index) => {
    record[key.trim().toLowerCase()] = values[index] ?? "";
  });
  for (const col of header) {
    if (!record[col]) record[col] = "";
  }
  return record;
});

/** Fields enrichment patches always replace when provided (curated corrections). */
const OVERWRITE_FIELDS = new Set<Column>([
  "description",
  "description_es",
  "phone",
  "email",
  "website",
  "address",
  "city",
  "served_counties",
  "coverage",
]);

let updated = 0;
for (const record of records) {
  const patch = enrichments[record.id];
  if (!patch) continue;

  for (const [key, value] of Object.entries(patch)) {
    if (value === undefined || value === null) continue;
    const trimmed = String(value).trim();
    if (!trimmed) continue;
    const existing = record[key]?.trim() ?? "";
    if (OVERWRITE_FIELDS.has(key as Column) || !existing) {
      record[key] = trimmed;
    }
  }
  updated++;
}

const outRows = [header, ...records.map((record) => header.map((col) => record[col] ?? ""))];
writeFileSync(CSV_PATH, serializeCsv(outRows));

console.log(`Applied enrichments to ${updated} resource(s) in ${CSV_PATH}`);
console.log(`Source: ${ENRICHMENT_PATH}`);
console.log("Next: regenerate seed SQL for the target state CSV.");
