import type { SupabaseClient } from "@supabase/supabase-js";
import {
  hasRestorablePreferences,
  parsePreferencesCookie,
  preferencesFromProfile,
  profileUpdateFromPreferences,
  restorePreferencesRecord,
  hasCompletedOnboarding,
} from "./parse";

export function profilePreferenceFieldsFromCookie(
  cookieRaw: string | undefined | null
): ReturnType<typeof profileUpdateFromPreferences> | null {
  const cookiePrefs = parsePreferencesCookie(cookieRaw ?? undefined);
  if (!cookiePrefs || !hasRestorablePreferences(cookiePrefs)) return null;
  return profileUpdateFromPreferences(restorePreferencesRecord(cookiePrefs));
}

export async function applyCookiePreferencesToProfileIfNeeded(
  supabase: SupabaseClient,
  userId: string,
  cookieRaw: string | undefined | null
): Promise<boolean> {
  const fields = profilePreferenceFieldsFromCookie(cookieRaw);
  if (!fields) return false;

  const { data: profile } = await supabase
    .from("profiles")
    .select("state, county, priority_categories, onboarding_completed_at")
    .eq("id", userId)
    .single();

  if (!profile) return false;

  const profilePrefs = preferencesFromProfile(profile);
  if (hasCompletedOnboarding(profilePrefs)) return false;

  const { error } = await supabase.from("profiles").update(fields).eq("id", userId);
  return !error;
}
