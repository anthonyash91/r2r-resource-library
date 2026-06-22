export const FACILITY_SESSION_COOKIE = "reentry_facility_ctx";
export const FACILITY_SESSION_MAX_AGE = Number(
  process.env.FACILITY_SESSION_MAX_AGE ?? 60 * 60 * 8
);

export interface FacilitySessionData {
  facilityId: string;
  pinHash: string;
  expiresAt: number;
}
