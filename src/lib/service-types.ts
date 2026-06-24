import { SERVICE_ALIASES } from "@/lib/service-aliases.generated";

/** Canonical service type labels used across resource CSVs. */
export const CANONICAL_SERVICES = [
  "Accessibility services",
  "Addiction treatment referrals",
  "Basic needs assistance",
  "Behavioral health services",
  "Benefits navigation",
  "Bus pass assistance",
  "Cash assistance (TANF)",
  "Child care assistance",
  "Children's services",
  "Civil legal representation",
  "Civil rights advocacy",
  "Clothing assistance",
  "Community supervision",
  "Computer and digital literacy",
  "Counseling",
  "Court compliance support",
  "Crisis services",
  "Developmental disability services",
  "Document assistance",
  "Domestic violence support",
  "Emergency shelter",
  "Employment assistance",
  "Expungement assistance",
  "Family reunification support",
  "Food pantry access",
  "GED and high school equivalency",
  "Housing legal aid",
  "Housing navigation",
  "Job readiness training",
  "Medicaid enrollment",
  "Parenting services",
  "Partner referrals",
  "Primary medical care",
  "Probation and parole supervision",
  "Reentry navigation",
  "Rent and utility assistance",
  "SNAP enrollment",
  "Senior services",
  "Sober living housing",
  "Spiritual support",
  "Substance use treatment",
  "Support groups",
  "Supportive housing",
  "Transitional housing",
  "Transportation assistance",
  "Veterans services",
  "Voting rights assistance",
  "Women's health services",
  "Workforce development",
] as const;

export type CanonicalService = (typeof CANONICAL_SERVICES)[number];

const CANONICAL_SET = new Set<string>(CANONICAL_SERVICES);

function aliasKey(value: string): string {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

/** Normalize a single service string to its canonical label. */
export function normalizeService(value: string): string {
  const trimmed = value.trim();
  if (!trimmed) return "";
  const key = aliasKey(trimmed);
  const mapped = SERVICE_ALIASES[key];
  if (mapped) return mapped;
  if (CANONICAL_SET.has(trimmed)) return trimmed;
  return trimmed;
}

/** Split on ``|``, normalize each token, dedupe preserving order. */
export function normalizeServices(raw: string | string[] | null | undefined): string[] {
  const parts = Array.isArray(raw)
    ? raw
    : (raw ?? "")
        .split("|")
        .map((part) => part.trim())
        .filter(Boolean);

  const seen = new Set<string>();
  const normalized: string[] = [];
  for (const part of parts) {
    const canonical = normalizeService(part);
    if (!canonical || seen.has(canonical)) continue;
    seen.add(canonical);
    normalized.push(canonical);
  }
  return normalized;
}

/** Join normalized services for CSV storage. */
export function normalizeServicesField(raw: string | null | undefined): string {
  return normalizeServices(raw).join("|");
}
