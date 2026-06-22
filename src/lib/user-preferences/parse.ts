import type { Profile } from "@/types";
import {
  MAX_PRIORITY_CATEGORIES,
  ONBOARDING_PRIORITY_SLUGS,
  isSupportedOnboardingState,
  isValidCountyForState,
} from "./constants";
import type { UserPreferences, UserPreferencesInput } from "./types";

export const EMPTY_PREFERENCES: UserPreferences = {
  state: null,
  county: null,
  priorityCategories: [],
  completedAt: null,
  skipped: false,
};

interface PrefsCookiePayload {
  state?: string | null;
  county?: string | null;
  priorityCategories?: string[];
  completedAt?: string | null;
  skipped?: boolean;
}

function normalizePrioritySlugs(values: unknown): string[] {
  if (!Array.isArray(values)) return [];
  const allowed = new Set<string>(ONBOARDING_PRIORITY_SLUGS);
  const seen = new Set<string>();
  const result: string[] = [];
  for (const value of values) {
    if (typeof value !== "string") continue;
    const slug = value.trim();
    if (!slug || !allowed.has(slug) || seen.has(slug)) continue;
    seen.add(slug);
    result.push(slug);
    if (result.length >= MAX_PRIORITY_CATEGORIES) break;
  }
  return result;
}

export function parsePreferencesCookie(raw: string | undefined | null): UserPreferences | null {
  if (!raw?.trim()) return null;
  try {
    const decoded = decodeURIComponent(raw);
    const payload = JSON.parse(decoded) as PrefsCookiePayload;
    return normalizePreferences({
      state: payload.state ?? null,
      county: payload.county ?? null,
      priorityCategories: payload.priorityCategories ?? [],
      completedAt: payload.completedAt ?? null,
      skipped: Boolean(payload.skipped),
    });
  } catch {
    return null;
  }
}

export function serializePreferencesCookie(prefs: UserPreferences): string {
  return encodeURIComponent(
    JSON.stringify({
      state: prefs.state,
      county: prefs.county,
      priorityCategories: prefs.priorityCategories,
      completedAt: prefs.completedAt,
      skipped: prefs.skipped,
    })
  );
}

export function normalizePreferences(prefs: UserPreferences): UserPreferences {
  const state =
    prefs.state && isSupportedOnboardingState(prefs.state) ? prefs.state : null;
  const county =
    state && prefs.county && isValidCountyForState(state, prefs.county)
      ? prefs.county
      : null;

  return {
    state,
    county,
    priorityCategories: normalizePrioritySlugs(prefs.priorityCategories),
    completedAt: prefs.completedAt ?? null,
    skipped: Boolean(prefs.skipped),
  };
}

export function preferencesFromProfile(profile: Pick<
  Profile,
  "state" | "county" | "priority_categories" | "onboarding_completed_at"
>): UserPreferences {
  return normalizePreferences({
    state: profile.state,
    county: profile.county,
    priorityCategories: profile.priority_categories ?? [],
    completedAt: profile.onboarding_completed_at ?? null,
    skipped: false,
  });
}

export function mergePreferences(
  cookiePrefs: UserPreferences | null,
  profilePrefs: UserPreferences | null
): UserPreferences {
  if (profilePrefs?.completedAt && profilePrefs.county && profilePrefs.state) {
    return profilePrefs;
  }
  if (cookiePrefs?.completedAt && cookiePrefs.county && cookiePrefs.state) {
    return cookiePrefs;
  }
  if (profilePrefs?.county && profilePrefs.state) {
    return normalizePreferences({
      ...EMPTY_PREFERENCES,
      ...profilePrefs,
      priorityCategories:
        profilePrefs.priorityCategories.length > 0
          ? profilePrefs.priorityCategories
          : cookiePrefs?.priorityCategories ?? [],
    });
  }
  if (cookiePrefs) return cookiePrefs;
  return { ...EMPTY_PREFERENCES };
}

export function validatePreferencesInput(input: UserPreferencesInput): UserPreferences | null {
  if (input.skipped) {
    return normalizePreferences({
      ...EMPTY_PREFERENCES,
      skipped: true,
    });
  }

  const state = input.state.trim();
  const county = input.county.trim();
  if (!isSupportedOnboardingState(state) || !isValidCountyForState(state, county)) {
    return null;
  }

  const priorityCategories = normalizePrioritySlugs(input.priorityCategories);
  if (!priorityCategories.length) return null;

  return normalizePreferences({
    state,
    county,
    priorityCategories,
    completedAt: new Date().toISOString(),
    skipped: false,
  });
}

export function needsOnboarding(prefs: UserPreferences | null): boolean {
  if (!prefs) return true;
  if (prefs.skipped) return false;
  return !hasCompletedOnboarding(prefs);
}

/** Show the optional onboarding banner (includes users who chose "skip for now"). */
export function shouldShowOnboardingPrompt(prefs: UserPreferences | null): boolean {
  return !hasCompletedOnboarding(prefs);
}

export function hasCompletedOnboarding(prefs: UserPreferences | null): boolean {
  if (!prefs?.completedAt || !prefs.state || !prefs.county) return false;
  return prefs.priorityCategories.length > 0;
}

export function hasPersonalizedPreferences(prefs: UserPreferences | null): boolean {
  return hasCompletedOnboarding(prefs);
}

export function profileUpdateFromPreferences(prefs: UserPreferences) {
  if (prefs.skipped) {
    return {
      state: null,
      county: null,
      priority_categories: [],
      onboarding_completed_at: null,
    };
  }

  return {
    state: prefs.state,
    county: prefs.county,
    priority_categories: prefs.priorityCategories,
    onboarding_completed_at: prefs.completedAt,
  };
}
