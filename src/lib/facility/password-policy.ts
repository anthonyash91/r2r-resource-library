/** ASVS V2.1.1 — minimum length for facility account passwords (signup / reset). */
export const FACILITY_MIN_PASSWORD_LENGTH = 12;

export function isFacilityPasswordValid(password: string): boolean {
  return password.length >= FACILITY_MIN_PASSWORD_LENGTH;
}
