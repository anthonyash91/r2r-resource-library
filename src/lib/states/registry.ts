import { INDIANA_COUNTIES } from "@/lib/indiana/counties";
import { KENTUCKY_COUNTIES } from "@/lib/kentucky/counties";
import { OHIO_COUNTIES } from "@/lib/ohio/counties";
import { MICHIGAN_COUNTIES } from "@/lib/michigan/counties";
import { TENNESSEE_COUNTIES } from "@/lib/tennessee/counties";
import { ILLINOIS_COUNTIES } from "@/lib/illinois/counties";
import { WEST_VIRGINIA_COUNTIES } from "@/lib/west-virginia/counties";
import { GEORGIA_COUNTIES } from "@/lib/georgia/counties";
import { NORTH_CAROLINA_COUNTIES } from "@/lib/north-carolina/counties";
import { VIRGINIA_COUNTIES } from "@/lib/virginia/counties";
import { SOUTH_CAROLINA_COUNTIES } from "@/lib/south-carolina/counties";
import { ALABAMA_COUNTIES } from "@/lib/alabama/counties";
import { ARIZONA_COUNTIES } from "@/lib/arizona/counties";
import { FLORIDA_COUNTIES } from "@/lib/florida/counties";
import { MISSISSIPPI_COUNTIES } from "@/lib/mississippi/counties";
import { WISCONSIN_COUNTIES } from "@/lib/wisconsin/counties";
import { TEXAS_COUNTIES } from "@/lib/texas/counties";

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
  { name: "Georgia", slug: "georgia", counties: GEORGIA_COUNTIES },
  { name: "North Carolina", slug: "north-carolina", counties: NORTH_CAROLINA_COUNTIES },
  { name: "Virginia", slug: "virginia", counties: VIRGINIA_COUNTIES },
  { name: "South Carolina", slug: "south-carolina", counties: SOUTH_CAROLINA_COUNTIES },
  { name: "Alabama", slug: "alabama", counties: ALABAMA_COUNTIES },
  { name: "Arizona", slug: "arizona", counties: ARIZONA_COUNTIES },
  { name: "Florida", slug: "florida", counties: FLORIDA_COUNTIES },
  { name: "Mississippi", slug: "mississippi", counties: MISSISSIPPI_COUNTIES },
  { name: "Wisconsin", slug: "wisconsin", counties: WISCONSIN_COUNTIES },
  { name: "Texas", slug: "texas", counties: TEXAS_COUNTIES },
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
