import { clearClientPreferences } from "@/lib/user-preferences/client";

export const TABLET_HANDOFF_PARAM = "facility_handoff";

/** Keys cleared on facility tablet handoff / facility sign-out. */
export const TABLET_LOCAL_STORAGE_KEYS = [
  "reentry_saved_resources",
  "reentry_recently_viewed",
  "reentry_session_id",
] as const;

const VIEW_DEDUPE_PREFIX = "reentry_view_logged:";

/** Remove on-device lists and prefs so the next inmate does not see the previous session. */
export function wipeTabletLocalState(): void {
  if (typeof window === "undefined") return;

  for (const key of TABLET_LOCAL_STORAGE_KEYS) {
    localStorage.removeItem(key);
  }

  const sessionKeys: string[] = [];
  for (let i = 0; i < sessionStorage.length; i++) {
    const key = sessionStorage.key(i);
    if (key?.startsWith(VIEW_DEDUPE_PREFIX)) {
      sessionKeys.push(key);
    }
  }
  for (const key of sessionKeys) {
    sessionStorage.removeItem(key);
  }

  clearClientPreferences();
}

export function stripTabletHandoffParam(pathname: string, search: string): string {
  const params = new URLSearchParams(search);
  params.delete(TABLET_HANDOFF_PARAM);
  const query = params.toString();
  return query ? `${pathname}?${query}` : pathname;
}
