import { PREFS_COOKIE, PREFS_COOKIE_MAX_AGE } from "./constants";
import { serializePreferencesCookie } from "./parse";
import type { UserPreferences } from "./types";

/** Set-Cookie value that clears onboarding preferences in route handlers. */
export function clearPreferencesSetCookie(): string {
  return `${PREFS_COOKIE}=; Path=/; Max-Age=0; SameSite=Lax`;
}

export function buildPreferencesSetCookie(prefs: UserPreferences): string {
  return `${PREFS_COOKIE}=${serializePreferencesCookie(prefs)}; Path=/; Max-Age=${PREFS_COOKIE_MAX_AGE}; SameSite=Lax`;
}
