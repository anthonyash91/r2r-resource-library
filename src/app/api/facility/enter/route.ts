import { NextResponse } from "next/server";
import { findFacilityBySiteId } from "@/lib/facility/data";
import {
  buildFacilitySessionData,
  facilitySessionCookieOptions,
  serializeFacilitySession,
} from "@/lib/facility/session";
import { FACILITY_SESSION_COOKIE } from "@/lib/facility/constants";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const facilityParam = url.searchParams.get("facility")?.trim();
  const pinParam = url.searchParams.get("pin")?.trim();
  const next = url.searchParams.get("next")?.trim() || "/";

  const redirectTarget = next.startsWith("/") ? next : "/";

  if (!facilityParam || !pinParam) {
    return NextResponse.redirect(new URL("/", url.origin));
  }

  const facility = await findFacilityBySiteId(facilityParam);
  if (!facility) {
    const failUrl = new URL(redirectTarget, url.origin);
    failUrl.searchParams.set("facility_error", "invalid");
    return NextResponse.redirect(failUrl);
  }

  const sessionData = buildFacilitySessionData(facility.id, pinParam);
  const response = NextResponse.redirect(new URL(redirectTarget, url.origin));
  response.cookies.set(
    FACILITY_SESSION_COOKIE,
    serializeFacilitySession(sessionData),
    facilitySessionCookieOptions()
  );

  return response;
}
