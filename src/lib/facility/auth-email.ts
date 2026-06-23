const FACILITY_AUTH_EMAIL_DOMAIN = "inmates.reentry.invalid";

/** Deterministic internal auth email for Supabase (not a real inbox). */
export function buildFacilityAuthEmail(facilityId: string, pinHash: string): string {
  return `${facilityId}+${pinHash}@${FACILITY_AUTH_EMAIL_DOMAIN}`;
}

export function isFacilityAuthEmail(email: string): boolean {
  return email.trim().toLowerCase().endsWith(`@${FACILITY_AUTH_EMAIL_DOMAIN}`);
}
