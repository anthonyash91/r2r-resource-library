import { KENTUCKY_COUNTIES } from "@/lib/kentucky/counties";
import { OHIO_COUNTIES } from "@/lib/ohio/counties";

export const PREFS_COOKIE = "reentry_prefs";
export const PREFS_COOKIE_MAX_AGE = 60 * 60 * 24 * 365;

export const MAX_PRIORITY_CATEGORIES = 3;

export const SUPPORTED_ONBOARDING_STATES = ["Kentucky", "Ohio"] as const;
export type OnboardingState = (typeof SUPPORTED_ONBOARDING_STATES)[number];

/** Curated category slugs shown during onboarding (most common reentry needs). */
export const ONBOARDING_PRIORITY_SLUGS = [
  "housing",
  "employment",
  "id-documentation",
  "financial-assistance",
  "substance-use-treatment",
  "legal-aid",
  "healthcare",
  "food-nutrition",
  "education",
  "reentry-organizations",
] as const;

export type OnboardingPrioritySlug = (typeof ONBOARDING_PRIORITY_SLUGS)[number];

const COUNTIES_BY_STATE: Record<OnboardingState, readonly string[]> = {
  Kentucky: KENTUCKY_COUNTIES,
  Ohio: OHIO_COUNTIES,
};

export function getCountiesForState(state: string): string[] {
  if (state === "Kentucky") return [...KENTUCKY_COUNTIES];
  if (state === "Ohio") return [...OHIO_COUNTIES];
  return [];
}

export function isSupportedOnboardingState(state: string): state is OnboardingState {
  return (SUPPORTED_ONBOARDING_STATES as readonly string[]).includes(state);
}

export function isValidCountyForState(state: string, county: string): boolean {
  if (!isSupportedOnboardingState(state)) return false;
  return COUNTIES_BY_STATE[state].includes(county);
}
