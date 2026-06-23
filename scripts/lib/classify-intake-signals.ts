import {
  INTAKE_SIGNALS,
  type IntakeSignal,
  isIntakeSignal,
} from "../../src/lib/intake-signals";

export type ResourceRowForIntake = {
  id?: string;
  name?: string;
  category?: string;
  description?: string;
  eligibility?: string;
  notes?: string;
  services?: string;
  tags?: string;
};

export type IntakeClassification = {
  signals: IntakeSignal[];
  confidence: "high" | "medium" | "low";
  reasons: Partial<Record<IntakeSignal, string>>;
};

function corpus(row: ResourceRowForIntake): string {
  return [
    row.name,
    row.category,
    row.description,
    row.eligibility,
    row.notes,
    row.services,
    row.tags,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function matchesAny(text: string, patterns: RegExp[]): boolean {
  return patterns.some((pattern) => pattern.test(text));
}

/** Programs that should not receive justice-involved intake tags. */
const EXCLUDE_ALL_SIGNALS = [
  /\b988\b/,
  /suicide.*crisis/,
  /crisis text line/,
  /crisis lifeline/,
  /\bhotline\b/,
  /phone line/,
  /navigation hub/,
  /information portal/,
  /online resource hub/,
  /not reentry-specific/,
  /available to anyone/,
  /referral resource for ohioans/,
  /this entry describes a navigation hub/,
  /does not replace direct services/,
  /state offices provide information and referrals statewide/,
  /findtreatment\.gov/,
  /samhsa online locator/,
  /official samhsa/,
  /provider search/,
];

const EXCLUDE_JUSTICE_SIGNALS = EXCLUDE_ALL_SIGNALS;

const ACCEPTS_CRIMINAL_RECORD = [
  /justice[- ]involved/,
  /criminal record/,
  /\bfelony\b/,
  /\breentry\b/,
  /expungement/,
  /fair[- ]chance/,
  /returning citizen/,
  /formerly incarcerat/,
  /released from (?:prison|incarceration)/,
  /people with convictions/,
  /record seal/,
  /record relief/,
  /halfway house/,
  /reentry service center/,
  /transitional work/,
  /doc[- ]contract/,
  /parole eligib/,
  /veterans treatment court/,
  /drug court/,
  /restored citizen/,
];

const ACCEPTS_CRIMINAL_RECORD_BLOCK = [
  /criminal record is (?:generally )?not a barrier/,
  /does not usually require a criminal-record disclosure/,
  /available to anyone in/,
  /open to all(?: ohio| kentucky)?/,
  /all ohioans/,
  /all kentuckians/,
  /information and referral only/,
];

const REFERRAL_REQUIRED = [
  /referral required/,
  /requires (?:an )?(?:institutional )?referral/,
  /by referral only/,
  /referral from (?:doc|the bureau|corrections|courts|parole|p(?:&|&amp;)p)/,
  /institutional referral/,
  /through the court system only/,
  /access is through the court/,
  /court[- ]ordered/,
  /court referral/,
  /referral through the court/,
  /must be referred/,
  /parole officer referral/,
  /referral from corrections/,
  /referral from courts/,
  /doc[- ]approved/,
  /state inmates near parole/,
];

const REFERRAL_BLOCK = [
  /self[- ]referral/,
  /no referral required/,
  /open self-referral/,
];

const WALK_IN_OK = [
  /walk[- ]in (?:hours|services|clinic|intake|welcome)/,
  /drop[- ]in (?:hours|services|clinic)/,
  /no appointment (?:necessary|required|needed)/,
  /open intake hours/,
  /for walk-in services/,
  /second chance community legal clinic/,
];

const WALK_IN_BLOCK = [
  /appointment required/,
  /by appointment only/,
  /call for appointment/,
  /not a walk-in/,
  /registration opens before/,
  /intake typically requires/,
  /central intake required before/,
  /whether walk-ins or referrals are accepted/,
  /walk-ins or referrals/,
  /confirm current intake steps/,
];

/** Rule-based classifier tuned for existing eligibility/notes prose.
 *  Python twin: scripts/lib/intake_signals.py */
export function classifyIntakeSignalsHeuristic(
  row: ResourceRowForIntake
): IntakeClassification {
  const text = corpus(row);
  const signals: IntakeSignal[] = [];
  const reasons: Partial<Record<IntakeSignal, string>> = {};
  let confidence: IntakeClassification["confidence"] = "high";

  if (matchesAny(text, EXCLUDE_ALL_SIGNALS)) {
    return { signals: [], confidence: "low", reasons: {} };
  }

  const excluded = matchesAny(text, EXCLUDE_JUSTICE_SIGNALS);

  if (
    !excluded &&
    matchesAny(text, ACCEPTS_CRIMINAL_RECORD) &&
    !matchesAny(text, ACCEPTS_CRIMINAL_RECORD_BLOCK)
  ) {
    signals.push("accepts_criminal_record");
    reasons.accepts_criminal_record = "reentry or criminal-record audience in text";
  }

  if (matchesAny(text, REFERRAL_REQUIRED) && !matchesAny(text, REFERRAL_BLOCK)) {
    signals.push("referral_required");
    reasons.referral_required = "referral or court/DOC gate in text";
  }

  if (
    matchesAny(text, WALK_IN_OK) &&
    !matchesAny(text, WALK_IN_BLOCK) &&
    !signals.includes("referral_required")
  ) {
    signals.push("walk_in_ok");
    reasons.walk_in_ok = "walk-in or drop-in language in text";
  } else if (matchesAny(text, WALK_IN_OK) && signals.includes("referral_required")) {
    confidence = "medium";
  }

  if (signals.length === 0) confidence = "low";

  return { signals, confidence, reasons };
}

export function serializeIntakeSignals(signals: IntakeSignal[]): string {
  return signals.join("|");
}

export function parseIntakeSignalsColumn(value: string | undefined): IntakeSignal[] {
  if (!value?.trim()) return [];
  return value
    .split("|")
    .map((part) => part.trim())
    .filter(isIntakeSignal);
}

export type LlmIntakeResult = {
  id: string;
  intake_signals: IntakeSignal[];
  rationale?: string;
};

const LLM_SYSTEM = `You tag reentry program listings with intake signals. Return JSON only.

Allowed intake_signals values (use only these, or an empty array):
- accepts_criminal_record — program explicitly serves justice-involved people or fair-chance/reentry populations (NOT generic public services open to everyone)
- referral_required — must come through DOC, parole, court, case manager, or another agency (not simple phone intake)
- walk_in_ok — can visit or access without a prior appointment/referral

Rules:
- A program may have multiple signals.
- Do NOT tag accepts_criminal_record for crisis lines (988), generic state info portals, or programs that only say "open to all".
- "Intake required" for legal aid is NOT referral_required unless another agency must send the client.
- Be conservative: empty array is fine when unclear.`;

export type LlmProvider = "anthropic" | "openai";

function buildLlmPayload(rows: ResourceRowForIntake[]) {
  return rows.map((row) => ({
    id: row.id,
    name: row.name,
    category: row.category,
    eligibility: row.eligibility,
    notes: row.notes,
    description: (row.description ?? "").slice(0, 400),
  }));
}

function parseLlmResults(content: string): LlmIntakeResult[] {
  const parsed = JSON.parse(content) as {
    results?: { id: string; intake_signals?: string[]; rationale?: string }[];
  };

  return (parsed.results ?? []).map((item) => ({
    id: item.id,
    intake_signals: (item.intake_signals ?? []).filter(isIntakeSignal),
    rationale: item.rationale,
  }));
}

export function resolveLlmProvider(
  args: string[]
): { provider: LlmProvider; apiKey: string } | null {
  const explicit = args.find((a) => a.startsWith("--llm-provider="))?.split("=")[1];
  if (explicit === "anthropic" || explicit === "openai") {
    const key =
      explicit === "anthropic"
        ? process.env.ANTHROPIC_API_KEY?.trim()
        : process.env.OPENAI_API_KEY?.trim();
    return key ? { provider: explicit, apiKey: key } : null;
  }

  if (process.env.ANTHROPIC_API_KEY?.trim()) {
    return { provider: "anthropic", apiKey: process.env.ANTHROPIC_API_KEY.trim() };
  }
  if (process.env.OPENAI_API_KEY?.trim()) {
    return { provider: "openai", apiKey: process.env.OPENAI_API_KEY.trim() };
  }
  return null;
}

async function classifyIntakeSignalsOpenAiBatch(
  rows: ResourceRowForIntake[],
  options: { apiKey: string; model?: string }
): Promise<LlmIntakeResult[]> {
  const model = options.model ?? process.env.OPENAI_MODEL ?? "gpt-4o-mini";
  const payload = buildLlmPayload(rows);

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${options.apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      temperature: 0.1,
      response_format: { type: "json_object" },
      messages: [
        { role: "system", content: LLM_SYSTEM },
        {
          role: "user",
          content: `Tag each resource. Respond with {"results":[{"id":"...","intake_signals":[],"rationale":"..."}]}\n\n${JSON.stringify(payload)}`,
        },
      ],
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`OpenAI API error ${response.status}: ${body}`);
  }

  const data = (await response.json()) as {
    choices?: { message?: { content?: string } }[];
  };
  const content = data.choices?.[0]?.message?.content;
  if (!content) throw new Error("OpenAI returned empty content");

  return parseLlmResults(content);
}

async function classifyIntakeSignalsAnthropicBatch(
  rows: ResourceRowForIntake[],
  options: { apiKey: string; model?: string }
): Promise<LlmIntakeResult[]> {
  const model =
    options.model ?? process.env.ANTHROPIC_MODEL ?? "claude-haiku-4-5-20251001";
  const payload = buildLlmPayload(rows);

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": options.apiKey,
      "anthropic-version": "2023-06-01",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      max_tokens: 4096,
      temperature: 0.1,
      system: LLM_SYSTEM,
      messages: [
        {
          role: "user",
          content: `Tag each resource. Respond with JSON only: {"results":[{"id":"...","intake_signals":[],"rationale":"..."}]}\n\n${JSON.stringify(payload)}`,
        },
      ],
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Anthropic API error ${response.status}: ${body}`);
  }

  const data = (await response.json()) as {
    content?: { type: string; text?: string }[];
  };
  const content = data.content?.find((block) => block.type === "text")?.text;
  if (!content) throw new Error("Anthropic returned empty content");

  const jsonText = content.replace(/^```json\s*/i, "").replace(/\s*```$/i, "").trim();
  return parseLlmResults(jsonText);
}

export async function classifyIntakeSignalsLlmBatch(
  rows: ResourceRowForIntake[],
  options: { provider: LlmProvider; apiKey: string; model?: string }
): Promise<LlmIntakeResult[]> {
  if (options.provider === "anthropic") {
    return classifyIntakeSignalsAnthropicBatch(rows, options);
  }
  return classifyIntakeSignalsOpenAiBatch(rows, options);
}

export function validateIntakeSignals(signals: string[]): IntakeSignal[] {
  return signals.filter(isIntakeSignal);
}

export { INTAKE_SIGNALS };
