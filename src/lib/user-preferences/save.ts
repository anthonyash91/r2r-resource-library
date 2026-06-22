"use client";

import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import {
  profileUpdateFromPreferences,
  validatePreferencesInput,
  writeClientPreferences,
  type UserPreferences,
  type UserPreferencesInput,
} from "@/lib/user-preferences";

export async function saveUserPreferences(
  input: UserPreferencesInput,
  userId?: string | null
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
    return { prefs };
  }

  const prefs = validatePreferencesInput(input);
  if (!prefs) {
    return { prefs: null, error: "invalid" };
  }

  writeClientPreferences(prefs);

  if (userId && isSupabaseConfigured()) {
    const supabase = createClient();
    if (supabase) {
      const { error } = await supabase
        .from("profiles")
        .update(profileUpdateFromPreferences(prefs))
        .eq("id", userId);

      if (error) {
        return { prefs: null, error: "save_failed" };
      }
    }
  }

  return { prefs };
}
