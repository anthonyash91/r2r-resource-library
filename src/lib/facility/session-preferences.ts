import { getFacilityProfilePreferencesByPinHash } from "@/lib/facility/data";
import { readFacilitySession } from "@/lib/facility/session";
import {
  hasRestorablePreferences,
  restorePreferencesRecord,
} from "@/lib/user-preferences/parse";
import type { UserPreferences } from "@/lib/user-preferences/types";

export async function getFacilitySessionProfilePreferences(
  facilityId: string,
  pinHash: string
): Promise<UserPreferences | null> {
  const prefs = await getFacilityProfilePreferencesByPinHash(facilityId, pinHash);
  if (!prefs || !hasRestorablePreferences(prefs)) return null;
  return restorePreferencesRecord(prefs);
}

export async function getServerFacilitySessionPreferences(): Promise<UserPreferences | null> {
  const session = await readFacilitySession();
  if (!session) return null;

  return getFacilitySessionProfilePreferences(session.facilityId, session.pinHash);
}
