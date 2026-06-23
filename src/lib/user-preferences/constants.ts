export {
  SUPPORTED_ONBOARDING_STATES,
  getCountiesForState,
  isSupportedOnboardingState,
  isValidCountyForState,
  type OnboardingState,
} from "@/lib/states/registry";

export const PREFS_COOKIE = "reentry_prefs";
export const PREFS_COOKIE_MAX_AGE = 60 * 60 * 24 * 365;

export const MAX_PRIORITY_CATEGORIES = 3;

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
