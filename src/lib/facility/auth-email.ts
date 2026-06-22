import { normalizePin } from "@/lib/facility/crypto";

const FACILITY_AUTH_EMAIL_DOMAIN = "inmates.reentry.invalid";

/** Deterministic internal auth email for Supabase (not a real inbox). */
export function buildFacilityAuthEmail(facilityId: string, pin: string): string {
  const normalizedPin = normalizePin(pin);
  return `${facilityId}+${normalizedPin}@${FACILITY_AUTH_EMAIL_DOMAIN}`;
}

export function isFacilityAuthEmail(email: string): boolean {
  return email.trim().toLowerCase().endsWith(`@${FACILITY_AUTH_EMAIL_DOMAIN}`);
}
