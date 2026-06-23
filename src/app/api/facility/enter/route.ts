import { NextResponse, type NextRequest } from "next/server";
import {
  facilityAccountExistsByPinHash,
  findFacilityBySiteId,
  verifyFacilityProfileBinding,
} from "@/lib/facility/data";
import { getFacilitySessionProfilePreferences } from "@/lib/facility/session-preferences";
import {
  buildFacilitySessionData,
  facilitySessionCookieOptions,
  parseFacilitySessionCookie,
  serializeFacilitySession,
} from "@/lib/facility/session";
import { FACILITY_SESSION_COOKIE } from "@/lib/facility/constants";
import { TABLET_HANDOFF_PARAM } from "@/lib/facility/tablet-handoff";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { isAdminClientConfigured } from "@/lib/supabase/admin";
import {
  buildPreferencesSetCookie,
  clearPreferencesSetCookie,
} from "@/lib/user-preferences/cookie-options";
import { safeInternalPath } from "@/lib/safe-redirect";

export async function GET(request: NextRequest) {
  const url = new URL(request.url);
  const facilityParam = url.searchParams.get("facility")?.trim();
  const pinParam = url.searchParams.get("pin")?.trim();
  const next = url.searchParams.get("next")?.trim() || "/";

  const redirectTarget = safeInternalPath(next, "/");

  if (!facilityParam || !pinParam) {
    return NextResponse.redirect(new URL("/", url.origin));
  }

  if (!isAdminClientConfigured()) {
    const failUrl = new URL(redirectTarget, url.origin);
    failUrl.searchParams.set("facility_error", "unconfigured");
    return NextResponse.redirect(failUrl);
  }

  let facility;
  try {
    facility = await findFacilityBySiteId(facilityParam);
  } catch {
    const failUrl = new URL(redirectTarget, url.origin);
    failUrl.searchParams.set("facility_error", "config");
    return NextResponse.redirect(failUrl);
  }

  if (!facility) {
    const failUrl = new URL(redirectTarget, url.origin);
    failUrl.searchParams.set("facility_error", "invalid");
    return NextResponse.redirect(failUrl);
  }

  const previousSession = parseFacilitySessionCookie(
    request.cookies.get(FACILITY_SESSION_COOKIE)?.value
  );

  const sessionData = buildFacilitySessionData(facility.id, pinParam);
  const pinChanged =
    previousSession !== null &&
    (previousSession.facilityId !== sessionData.facilityId ||
      previousSession.pinHash !== sessionData.pinHash);

  let needsHandoff = pinChanged;

  if (isSupabaseConfigured()) {
    const supabase = await createClient();
    if (supabase) {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (user) {
        const bound = await verifyFacilityProfileBinding(
          user.id,
          sessionData.facilityId,
          sessionData.pinHash
        );
        if (!bound) {
          await supabase.auth.signOut();
          needsHandoff = true;
        }
      }
    }
  }

  const redirectUrl = new URL(redirectTarget, url.origin);
  if (needsHandoff) {
    redirectUrl.searchParams.set(TABLET_HANDOFF_PARAM, "1");
  }

  const hasAccount = await facilityAccountExistsByPinHash(
    sessionData.facilityId,
    sessionData.pinHash
  );
  const profilePreferences = hasAccount
    ? await getFacilitySessionProfilePreferences(sessionData.facilityId, sessionData.pinHash)
    : null;

  const response = NextResponse.redirect(redirectUrl);
  response.cookies.set(
    FACILITY_SESSION_COOKIE,
    serializeFacilitySession(sessionData),
    facilitySessionCookieOptions()
  );

  if (needsHandoff) {
    response.headers.append("Set-Cookie", clearPreferencesSetCookie());
  }

  if (profilePreferences) {
    response.headers.append("Set-Cookie", buildPreferencesSetCookie(profilePreferences));
  }

  return response;
}
