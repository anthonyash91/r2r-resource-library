import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { PREFS_COOKIE } from "./constants";
import {
  mergePreferences,
  parsePreferencesCookie,
  preferencesFromProfile,
} from "./parse";
import type { UserPreferences } from "./types";

export async function getServerUserPreferences(): Promise<UserPreferences> {
  const cookieStore = await cookies();
  const cookiePrefs = parsePreferencesCookie(cookieStore.get(PREFS_COOKIE)?.value);

  if (!isSupabaseConfigured()) {
    return mergePreferences(cookiePrefs, null);
  }

  const supabase = await createClient();
  if (!supabase) {
    return mergePreferences(cookiePrefs, null);
  }

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return mergePreferences(cookiePrefs, null);
  }

  const { data: profile } = await supabase
    .from("profiles")
    .select("state, county, priority_categories, onboarding_completed_at")
    .eq("id", user.id)
    .single();

  const profilePrefs = profile ? preferencesFromProfile(profile) : null;
  return mergePreferences(cookiePrefs, profilePrefs);
}
