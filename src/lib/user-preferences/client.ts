"use client";

import { PREFS_COOKIE, PREFS_COOKIE_MAX_AGE } from "./constants";
import { parsePreferencesCookie, serializePreferencesCookie } from "./parse";
import type { UserPreferences } from "./types";

export function readClientPreferences(): UserPreferences | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(
    new RegExp(`(?:^|; )${PREFS_COOKIE}=([^;]*)`)
  );
  if (!match?.[1]) return null;
  return parsePreferencesCookie(match[1]);
}

export function writeClientPreferences(prefs: UserPreferences) {
  if (typeof document === "undefined") return;
  const value = serializePreferencesCookie(prefs);
  document.cookie = `${PREFS_COOKIE}=${value};path=/;max-age=${PREFS_COOKIE_MAX_AGE};samesite=lax`;
}

export function clearClientPreferences() {
  if (typeof document === "undefined") return;
  document.cookie = `${PREFS_COOKIE}=;path=/;max-age=0;samesite=lax`;
}
