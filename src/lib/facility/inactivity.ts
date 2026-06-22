/** Client-safe inactivity timeout (ms). Override with NEXT_PUBLIC_FACILITY_INACTIVITY_MS. */
export const FACILITY_INACTIVITY_MS = Number(
  process.env.NEXT_PUBLIC_FACILITY_INACTIVITY_MS ?? 30 * 60 * 1000
);
