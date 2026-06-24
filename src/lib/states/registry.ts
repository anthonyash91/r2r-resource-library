import { INDIANA_COUNTIES } from "@/lib/indiana/counties";
import { KENTUCKY_COUNTIES } from "@/lib/kentucky/counties";
import { OHIO_COUNTIES } from "@/lib/ohio/counties";
import { MICHIGAN_COUNTIES } from "@/lib/michigan/counties";
import { TENNESSEE_COUNTIES } from "@/lib/tennessee/counties";
import { ILLINOIS_COUNTIES } from "@/lib/illinois/counties";
import { WEST_VIRGINIA_COUNTIES } from "@/lib/west-virginia/counties";

export interface OnboardingStateConfig {
  /** Full name stored in the database and user preferences. */
  name: string;
  /** i18n slug for onboarding.states.{slug} and pathways.firstWeek.introByState.{slug}. */
  slug: string;
  counties: readonly string[];
}

/**
 * Deployed states with resource data and onboarding support.
 * To add a state: create src/lib/{slug}/counties.ts, append an entry here,
 * and add matching keys in en.ts / es.ts under onboarding.states and
 * pathways.firstWeek.introByState. County map centroids for new states are
 * picked up automatically on `npm run build` via scripts/generate-us-map-data.py.
 */
export const ONBOARDING_STATE_REGISTRY = [
  { name: "Kentucky", slug: "kentucky", counties: KENTUCKY_COUNTIES },
  { name: "Ohio", slug: "ohio", counties: OHIO_COUNTIES },
  { name: "Indiana", slug: "indiana", counties: INDIANA_COUNTIES },
  { name: "Tennessee", slug: "tennessee", counties: TENNESSEE_COUNTIES },
  { name: "Michigan", slug: "michigan", counties: MICHIGAN_COUNTIES },
  { name: "Illinois", slug: "illinois", counties: ILLINOIS_COUNTIES },
  { name: "West Virginia", slug: "west-virginia", counties: WEST_VIRGINIA_COUNTIES },
] as const satisfies readonly OnboardingStateConfig[];

export type OnboardingState = (typeof ONBOARDING_STATE_REGISTRY)[number]["name"];

export const SUPPORTED_ONBOARDING_STATES: readonly OnboardingState[] =
  ONBOARDING_STATE_REGISTRY.map((entry) => entry.name);

const registryByName = new Map<string, OnboardingStateConfig>(
  ONBOARDING_STATE_REGISTRY.map((entry) => [entry.name, entry])
);

export function getOnboardingStateConfig(state: string): OnboardingStateConfig | undefined {
  return registryByName.get(state);
}

export function getCountiesForState(state: string): string[] {
  const entry = registryByName.get(state);
  return entry ? [...entry.counties] : [];
}

export function isSupportedOnboardingState(state: string): state is OnboardingState {
  return registryByName.has(state);
}

export function isValidCountyForState(state: string, county: string): boolean {
  const entry = registryByName.get(state);
  return entry ? entry.counties.includes(county) : false;
}

export function getPathwayIntroKey(state: string | null | undefined): string {
  const entry = state ? registryByName.get(state) : undefined;
  if (entry) return `pathways.firstWeek.introByState.${entry.slug}`;
  return "pathways.firstWeek.introDefault";
}
