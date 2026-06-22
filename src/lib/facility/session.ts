import { cookies } from "next/headers";
import {
  decryptFacilitySessionPayload,
  encryptFacilitySessionPayload,
  hashInmatePin,
  normalizePin,
} from "@/lib/facility/crypto";
import {
  FACILITY_SESSION_COOKIE,
  FACILITY_SESSION_MAX_AGE,
  type FacilitySessionData,
} from "@/lib/facility/constants";

function parseSessionPayload(raw: string): FacilitySessionData | null {
  const decrypted = decryptFacilitySessionPayload(raw);
  if (!decrypted) return null;

  try {
    const parsed = JSON.parse(decrypted) as FacilitySessionData;
    if (!parsed.facilityId || !parsed.pinHash || !parsed.expiresAt) return null;
    if (!parsed.pin) return null;
    if (parsed.expiresAt < Date.now()) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function buildFacilitySessionData(
  facilityId: string,
  pin: string
): FacilitySessionData {
  return {
    facilityId,
    pinHash: hashInmatePin(facilityId, pin),
    pin: normalizePin(pin),
    expiresAt: Date.now() + FACILITY_SESSION_MAX_AGE * 1000,
  };
}

export function serializeFacilitySession(data: FacilitySessionData): string {
  return encryptFacilitySessionPayload(JSON.stringify(data));
}

export async function readFacilitySession(): Promise<FacilitySessionData | null> {
  const cookieStore = await cookies();
  const raw = cookieStore.get(FACILITY_SESSION_COOKIE)?.value;
  return parseFacilitySessionCookie(raw);
}

export function parseFacilitySessionCookie(raw: string | undefined): FacilitySessionData | null {
  if (!raw) return null;
  return parseSessionPayload(raw);
}

export function facilitySessionCookieOptions() {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    maxAge: FACILITY_SESSION_MAX_AGE,
  };
}

export function clearFacilitySessionCookieOptions() {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    maxAge: 0,
  };
}
