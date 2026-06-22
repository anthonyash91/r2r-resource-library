"use client";

import { isSupabaseConfigured } from "@/lib/supabase/client";
import {
  validatePreferencesInput,
  writeClientPreferences,
  type UserPreferences,
  type UserPreferencesInput,
} from "@/lib/user-preferences";

async function savePreferencesToProfile(
  input: UserPreferencesInput
): Promise<{ ok: boolean; prefs: UserPreferences | null }> {
  const response = await fetch("/api/user/preferences", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });

  if (response.status === 401) {
    return { ok: true, prefs: null };
  }

  if (!response.ok) {
    return { ok: false, prefs: null };
  }

  const payload = (await response.json()) as { prefs?: UserPreferences };
  return { ok: true, prefs: payload.prefs ?? null };
}

export async function saveUserPreferences(
  input: UserPreferencesInput,
  _userId?: string | null
): Promise<{ prefs: UserPreferences | null; error?: string }> {
  if (input.skipped) {
    const prefs = validatePreferencesInput({
      state: "",
      county: "",
      priorityCategories: [],
      skipped: true,
    });
    if (!prefs) return { prefs: null, error: "invalid" };
    writeClientPreferences(prefs);

    if (isSupabaseConfigured()) {
      const { ok } = await savePreferencesToProfile(input);
      if (!ok) return { prefs: null, error: "save_failed" };
    }

    return { prefs };
  }

  const prefs = validatePreferencesInput(input);
  if (!prefs) {
    return { prefs: null, error: "invalid" };
  }

  writeClientPreferences(prefs);

  if (isSupabaseConfigured()) {
    const { ok, prefs: savedPrefs } = await savePreferencesToProfile(input);
    if (!ok) return { prefs: null, error: "save_failed" };
    if (savedPrefs) {
      writeClientPreferences(savedPrefs);
      return { prefs: savedPrefs };
    }
  }

  return { prefs };
}
