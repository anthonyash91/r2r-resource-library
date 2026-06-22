import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import { hashInmatePin, normalizePin } from "@/lib/facility/crypto";
import { getFacilityProfileRecoveryByPinHash } from "@/lib/facility/data";
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

  let body: { pin?: string } = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const pin = normalizePin(body.pin ?? "");
  if (!pin) {
    return NextResponse.json({ error: t("facility.resetPinRequired") }, { status: 400 });
  }

  const pinHash = hashInmatePin(session.facilityId, pin);
  const profile = await getFacilityProfileRecoveryByPinHash(session.facilityId, pinHash);

  if (!profile) {
    return NextResponse.json({ error: t("facility.resetPinInvalid") }, { status: 403 });
  }

  return NextResponse.json({
    recoveryQuestion1: profile.recovery_question_1,
    recoveryQuestion2: profile.recovery_question_2,
  });
}
