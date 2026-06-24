import type { Resource } from "@/types";

/** Canonical intake signal keys stored in DB / CSV. */
export const INTAKE_SIGNALS = [
  "accepts_criminal_record",
  "referral_required",
  "walk_in_ok",
] as const;

export type IntakeSignal = (typeof INTAKE_SIGNALS)[number];

const INTAKE_SIGNAL_SET = new Set<string>(INTAKE_SIGNALS);

export function isIntakeSignal(value: string): value is IntakeSignal {
  return INTAKE_SIGNAL_SET.has(value);
}

export function getResourceIntakeSignals(
  resource: Pick<Resource, "intake_signals">
): IntakeSignal[] {
  const signals = resource.intake_signals ?? [];
  return signals.filter(isIntakeSignal);
}

/** Parse `intake` query param (pipe-separated signal keys). */
export function parseIntakeFilterParam(value: string | null | undefined): IntakeSignal[] {
  if (!value?.trim()) return [];
  return value
    .split("|")
    .map((part) => part.trim())
    .filter(isIntakeSignal);
}

export function serializeIntakeFilterParam(signals: IntakeSignal[]): string {
  return signals.join("|");
}

export function resourceMatchesIntakeFilters(
  resource: Pick<Resource, "intake_signals">,
  required: IntakeSignal[]
): boolean {
  if (required.length === 0) return true;
  const present = new Set(getResourceIntakeSignals(resource));
  return required.every((signal) => present.has(signal));
}

export function filterResourcesByIntakeSignals<T extends Pick<Resource, "intake_signals">>(
  resources: T[],
  required: IntakeSignal[]
): T[] {
  if (required.length === 0) return resources;
  return resources.filter((resource) => resourceMatchesIntakeFilters(resource, required));
}

export function countResourcesByIntakeSignal(
  resources: Pick<Resource, "intake_signals">[]
): Record<IntakeSignal, number> {
  const counts = Object.fromEntries(
    INTAKE_SIGNALS.map((signal) => [signal, 0])
  ) as Record<IntakeSignal, number>;

  for (const resource of resources) {
    for (const signal of getResourceIntakeSignals(resource)) {
      counts[signal] += 1;
    }
  }

  return counts;
}
