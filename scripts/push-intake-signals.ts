/**
 * Push intake_signals from state CSVs into Supabase (by seed UUID row order).
 *
 * Usage:
 *   npx tsx scripts/push-intake-signals.ts
 *   npm run db:push:intake
 */
import { readFileSync, existsSync } from "fs";
import { resolve } from "path";
import { createClient } from "@supabase/supabase-js";
import { isIntakeSignal } from "../src/lib/intake-signals";

function loadEnvLocal() {
  const path = resolve(process.cwd(), ".env.local");
  if (!existsSync(path)) return;
  for (const line of readFileSync(path, "utf8").split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    let value = trimmed.slice(eq + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (!process.env[key]) process.env[key] = value;
  }
}

loadEnvLocal();

const BATCH_SIZE = 50;

const SOURCES = [
  { csv: "data/resources.csv", uuidPrefix: "d1000001" },
  { csv: "data/ohio-resources.csv", uuidPrefix: "d2000001" },
  { csv: "data/indiana-resources.csv", uuidPrefix: "d3000001" },
] as const;

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

function resourceUuid(prefix: string, index: number) {
  return `${prefix}-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`;
}

function parseIntakeSignals(value: string): string[] {
  if (!value.trim()) return [];
  return value
    .split(/[|]/)
    .map((part) => part.trim())
    .filter(isIntakeSignal);
}

async function main() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !serviceKey) {
    console.error("Missing NEXT_PUBLIC_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env.local");
    process.exit(1);
  }

  const supabase = createClient(url, serviceKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  const updates: { id: string; intake_signals: string[] }[] = [];

  for (const source of SOURCES) {
    const csvPath = resolve(process.cwd(), source.csv);
    const raw = readFileSync(csvPath, "utf8");
    const rows = parseCsv(raw);
    const headers = rows[0].map((h) => h.trim().toLowerCase());
    const intakeIdx = headers.indexOf("intake_signals");
    if (intakeIdx === -1) {
      console.warn(`No intake_signals column in ${source.csv} — skipping`);
      continue;
    }

    rows.slice(1).forEach((values, index) => {
      const signals = parseIntakeSignals(values[intakeIdx] ?? "");
      if (signals.length === 0) return;
      updates.push({
        id: resourceUuid(source.uuidPrefix, index),
        intake_signals: signals,
      });
    });
  }

  console.log(`Updating intake_signals on ${updates.length} resource(s)...`);

  let done = 0;
  for (let i = 0; i < updates.length; i += BATCH_SIZE) {
    const batch = updates.slice(i, i + BATCH_SIZE);
    for (const row of batch) {
      const { error } = await supabase
        .from("resources")
        .update({ intake_signals: row.intake_signals })
        .eq("id", row.id);
      if (error) {
        console.error(`Failed on ${row.id}:`, error.message);
        if (error.message.includes("intake_signals")) {
          console.error("Run migration 014_add_intake_signals.sql first.");
        }
        process.exit(1);
      }
      done++;
    }
    console.log(`  ${done}/${updates.length}`);
  }

  const { count } = await supabase
    .from("resources")
    .select("*", { count: "exact", head: true })
    .not("intake_signals", "eq", "{}");

  console.log(`Done. Resources with intake signals: ${count ?? done}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
