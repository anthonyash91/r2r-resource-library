import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import {
  clearFacilityResetCookieOptions,
  readFacilityReset,
} from "@/lib/facility/reset-session";
import { FACILITY_RESET_COOKIE } from "@/lib/facility/constants";
import { readFacilitySession } from "@/lib/facility/session";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

export async function POST(request: Request) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const admin = createAdminClient();
  if (!admin) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const session = await readFacilitySession();
  if (!session) {
    return NextResponse.json({ error: t("facility.sessionRequired") }, { status: 401 });
  }

  const reset = await readFacilityReset();
  if (!reset || reset.facilityId !== session.facilityId) {
    return NextResponse.json({ error: t("facility.resetVerificationExpired") }, { status: 403 });
  }

  let body: { password?: string } = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const password = body.password ?? "";
  if (password.length < 8) {
    return NextResponse.json({ error: t("facility.resetInvalid") }, { status: 400 });
  }

  const { data: profile, error: profileError } = await admin
    .from("profiles")
    .select("id, email")
    .eq("signup_context", "facility")
    .eq("facility_id", reset.facilityId)
    .eq("inmate_pin_hash", reset.pinHash)
    .maybeSingle();

  if (profileError || !profile) {
    return NextResponse.json({ error: t("facility.resetFailed") }, { status: 400 });
  }

  const { error: updateError } = await admin.auth.admin.updateUserById(profile.id, {
    password,
  });

  if (updateError) {
    return NextResponse.json({ error: t("facility.resetFailed") }, { status: 500 });
  }

  const cookieStore = await cookies();
  cookieStore.set(FACILITY_RESET_COOKIE, "", clearFacilityResetCookieOptions());

  return NextResponse.json({ success: true });
}
