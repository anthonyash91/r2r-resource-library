import { cookies } from "next/headers";
import {
  decryptFacilitySessionPayload,
  encryptFacilitySessionPayload,
} from "@/lib/facility/crypto";
import {
  FACILITY_RESET_COOKIE,
  FACILITY_RESET_MAX_AGE,
} from "@/lib/facility/constants";

export interface FacilityResetData {
  facilityId: string;
  pinHash: string;
  expiresAt: number;
}

function parseResetPayload(raw: string): FacilityResetData | null {
  const decrypted = decryptFacilitySessionPayload(raw);
  if (!decrypted) return null;

  try {
    const parsed = JSON.parse(decrypted) as FacilityResetData;
    if (!parsed.facilityId || !parsed.pinHash || !parsed.expiresAt) return null;
    if (parsed.expiresAt < Date.now()) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function serializeFacilityReset(data: FacilityResetData): string {
  return encryptFacilitySessionPayload(JSON.stringify(data));
}

export async function readFacilityReset(): Promise<FacilityResetData | null> {
  const cookieStore = await cookies();
  const raw = cookieStore.get(FACILITY_RESET_COOKIE)?.value;
  if (!raw) return null;
  return parseResetPayload(raw);
}

export function buildFacilityResetData(facilityId: string, pinHash: string): FacilityResetData {
  return {
    facilityId,
    pinHash,
    expiresAt: Date.now() + FACILITY_RESET_MAX_AGE * 1000,
  };
}

export function facilityResetCookieOptions() {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    maxAge: FACILITY_RESET_MAX_AGE,
  };
}

export function clearFacilityResetCookieOptions() {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    maxAge: 0,
  };
}
