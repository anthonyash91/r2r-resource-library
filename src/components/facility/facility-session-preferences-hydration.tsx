"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import {
  hasCompletedOnboarding,
  readClientPreferences,
  restorePreferencesRecord,
  writeClientPreferences,
  type UserPreferences,
} from "@/lib/user-preferences";

export const PREFS_UPDATED_EVENT = "reentry-prefs-updated";

export function FacilitySessionPreferencesHydration() {
  const { user, loading } = useAuth();
  const pathname = usePathname();

  useEffect(() => {
    if (loading || user) return;

    void (async () => {
      const response = await fetch("/api/facility/status");
      if (!response.ok) return;

      const data = (await response.json()) as { preferences?: UserPreferences | null };
      const prefs = data.preferences ? restorePreferencesRecord(data.preferences) : null;
      if (!prefs || !hasCompletedOnboarding(prefs)) return;

      const current = readClientPreferences();
      if (hasCompletedOnboarding(current)) return;

      writeClientPreferences(prefs);
      window.dispatchEvent(new Event(PREFS_UPDATED_EVENT));
    })();
  }, [loading, user, pathname]);

  return null;
}
