/**
 * Auto-tag resources with intake_signals from eligibility/notes text.
 *
 * Usage:
 *   npx tsx scripts/tag-intake-signals.ts data/kentucky-resources.csv
 *   npx tsx scripts/tag-intake-signals.ts data/ohio-resources.csv
 *   npx tsx scripts/tag-intake-signals.ts data/kentucky-resources.csv --dry-run
 *   npx tsx scripts/tag-intake-signals.ts data/kentucky-resources.csv --llm
 *   npx tsx scripts/tag-intake-signals.ts data/kentucky-resources.csv --llm --llm-provider=anthropic
 *
 * Heuristic mode (default): free, instant, no API key.
 * --llm: uses ANTHROPIC_API_KEY (preferred) or OPENAI_API_KEY. Falls back to heuristics if neither is set.
 * Note: a Claude.ai Pro/Max subscription is separate from the Anthropic API — scripts cannot use the web sub.
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import { resolve } from "path";
import {
  classifyIntakeSignalsHeuristic,
  classifyIntakeSignalsLlmBatch,
  resolveLlmProvider,
  serializeIntakeSignals,
  type ResourceRowForIntake,
} from "./lib/classify-intake-signals";

function loadEnvLocal() {
  const envPath = resolve(process.cwd(), ".env.local");
  if (!existsSync(envPath)) return;
  for (const line of readFileSync(envPath, "utf8").split("\n")) {
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

const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const useLlm = args.includes("--llm");
const writeJsonIdx = args.indexOf("--write-json");
const jsonOut =
  writeJsonIdx >= 0 ? resolve(process.cwd(), args[writeJsonIdx + 1]) : null;
const csvPath = resolve(
  process.cwd(),
  args.find((a) => !a.startsWith("--") && a.endsWith(".csv")) ?? "data/kentucky-resources.csv"
);

const BATCH_SIZE = 15;

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

async function main() {
  const raw = readFileSync(csvPath, "utf8");
  const rows = parseCsv(raw);
  if (rows.length < 2) {
    console.error(`No data rows in ${csvPath}`);
    process.exit(1);
  }

  const header = rows[0].map((h) => h.trim().toLowerCase());
  if (!header.includes("intake_signals")) header.push("intake_signals");
  const intakeCol = header.indexOf("intake_signals");

  const records: Record<string, string>[] = rows.slice(1).map((values) => {
    const record: Record<string, string> = {};
    rows[0].forEach((key, index) => {
      record[key.trim().toLowerCase()] = values[index] ?? "";
    });
    for (const col of header) {
      if (!record[col]) record[col] = "";
    }
    return record;
  });

  const enrichmentPatch: Record<string, { intake_signals: string }> = {};
  const stats = {
    tagged: 0,
    accepts: 0,
    referral: 0,
    walkIn: 0,
    unchanged: 0,
    lowConfidence: 0,
  };

  const llmConfig = useLlm ? resolveLlmProvider(args) : null;
  const llmActive = Boolean(llmConfig);

  if (useLlm && !llmConfig) {
    console.warn(
      "No ANTHROPIC_API_KEY or OPENAI_API_KEY — using heuristics only. (Claude.ai subscription does not replace API keys.)"
    );
  }

  if (llmActive && llmConfig) {
    for (let i = 0; i < records.length; i += BATCH_SIZE) {
      const batch = records.slice(i, i + BATCH_SIZE);
      const llmRows: ResourceRowForIntake[] = batch.map((r) => ({
        id: r.id,
        name: r.name,
        category: r.category,
        description: r.description,
        eligibility: r.eligibility,
        notes: r.notes,
        services: r.services,
        tags: r.tags,
      }));

      const results = await classifyIntakeSignalsLlmBatch(llmRows, llmConfig);
      const byId = new Map(results.map((r) => [r.id, r]));

      for (const record of batch) {
        const llm = byId.get(record.id);
        const signals = llm?.intake_signals ?? classifyIntakeSignalsHeuristic(record).signals;
        const serialized = serializeIntakeSignals(signals);
        if (serialized !== record.intake_signals) {
          record.intake_signals = serialized;
          enrichmentPatch[record.id] = { intake_signals: serialized };
          stats.tagged++;
        } else {
          stats.unchanged++;
        }
        if (signals.includes("accepts_criminal_record")) stats.accepts++;
        if (signals.includes("referral_required")) stats.referral++;
        if (signals.includes("walk_in_ok")) stats.walkIn++;
      }

      console.log(`LLM batch ${Math.floor(i / BATCH_SIZE) + 1}: ${batch.length} rows`);
    }
  } else {
    for (const record of records) {
      const { signals, confidence } = classifyIntakeSignalsHeuristic(record);
      const serialized = serializeIntakeSignals(signals);
      if (confidence === "low" && signals.length === 0) stats.lowConfidence++;

      if (serialized !== record.intake_signals) {
        record.intake_signals = serialized;
        enrichmentPatch[record.id] = { intake_signals: serialized };
        stats.tagged++;
      } else {
        stats.unchanged++;
      }
      if (signals.includes("accepts_criminal_record")) stats.accepts++;
      if (signals.includes("referral_required")) stats.referral++;
      if (signals.includes("walk_in_ok")) stats.walkIn++;
    }
  }

  console.log(`\n${csvPath}`);
  console.log(`  mode: ${llmActive && llmConfig ? `llm (${llmConfig.provider})` : "heuristic"}`);
  console.log(`  rows: ${records.length}`);
  console.log(`  updated: ${stats.tagged}`);
  console.log(`  unchanged: ${stats.unchanged}`);
  console.log(`  accepts_criminal_record: ${stats.accepts}`);
  console.log(`  referral_required: ${stats.referral}`);
  console.log(`  walk_in_ok: ${stats.walkIn}`);
  console.log(`  no signals (heuristic low-confidence): ${stats.lowConfidence}`);

  if (dryRun) {
    const sample = records
      .filter((r) => r.intake_signals)
      .slice(0, 8)
      .map((r) => `  ${r.id} ${r.name?.slice(0, 40)} → ${r.intake_signals}`);
    if (sample.length) {
      console.log("\nSample tags:");
      console.log(sample.join("\n"));
    }
    console.log("\nDry run — CSV not written.");
    return;
  }

  const outRows = [header, ...records.map((record) => header.map((col) => record[col] ?? ""))];
  writeFileSync(csvPath, serializeCsv(outRows));
  console.log(`\nWrote ${csvPath}`);

  if (jsonOut) {
    writeFileSync(jsonOut, JSON.stringify(enrichmentPatch, null, 2) + "\n");
    console.log(`Wrote audit JSON: ${jsonOut}`);
  }

  console.log("\nNext: npm run seed:resources:kentucky (or seed:resources:ohio) to regenerate SQL.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
