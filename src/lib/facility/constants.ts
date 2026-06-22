export const FACILITY_SESSION_COOKIE = "reentry_facility_ctx";
export const FACILITY_RESET_COOKIE = "reentry_facility_reset";
export const FACILITY_SESSION_MAX_AGE = Number(
  process.env.FACILITY_SESSION_MAX_AGE ?? 60 * 60 * 8
);
export const FACILITY_RESET_MAX_AGE = 15 * 60;

export interface FacilitySessionData {
  facilityId: string;
  pinHash: string;
  pin: string;
  expiresAt: number;
}
