"use client";

import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import {
  hasCompletedOnboarding,
  preferencesFromProfile,
  readClientPreferences,
  writeClientPreferences,
} from "@/lib/user-preferences";
import { profileUpdateFromPreferences } from "@/lib/user-preferences/parse";

export async function syncCookiePreferencesToProfile(userId: string): Promise<void> {
  if (!isSupabaseConfigured()) return;

  const cookiePrefs = readClientPreferences();
  if (!hasCompletedOnboarding(cookiePrefs)) return;

  const supabase = createClient();
  if (!supabase) return;

  const { data: profile } = await supabase
    .from("profiles")
    .select("state, county, priority_categories, onboarding_completed_at")
    .eq("id", userId)
    .single();

  if (!profile) return;

  const profilePrefs = preferencesFromProfile(profile);
  if (hasCompletedOnboarding(profilePrefs)) return;

  const update = profileUpdateFromPreferences(cookiePrefs!);
  const { error } = await supabase.from("profiles").update(update).eq("id", userId);

  if (!error) {
    writeClientPreferences(cookiePrefs!);
  }
}
