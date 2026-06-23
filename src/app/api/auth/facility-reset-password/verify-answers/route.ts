import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import {
  hashInmatePin,
  hashRecoveryAnswer,
  normalizePin,
  secureCompareHex,
} from "@/lib/facility/crypto";
import { getFacilityProfileRecoveryByPinHash } from "@/lib/facility/data";
import {
  buildFacilityResetData,
  facilityResetCookieOptions,
  serializeFacilityReset,
} from "@/lib/facility/reset-session";
import { FACILITY_RESET_COOKIE } from "@/lib/facility/constants";
import { readFacilitySession } from "@/lib/facility/session";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";
import { checkRateLimit, getRequestClientIp } from "@/lib/rate-limit";

const ANSWERS_VERIFY_LIMIT = { maxAttempts: 5, windowMs: 15 * 60 * 1000 };

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

  let body: { pin?: string; answer1?: string; answer2?: string } = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const pin = normalizePin(body.pin ?? "");
  const answer1 = body.answer1 ?? "";
  const answer2 = body.answer2 ?? "";

  if (!pin || !answer1 || !answer2) {
    return NextResponse.json({ error: t("facility.resetInvalid") }, { status: 400 });
  }

  const pinHash = hashInmatePin(session.facilityId, pin);
  const rateKey = `facility-reset-answers:${session.facilityId}:${pinHash}:${getRequestClientIp(request)}`;
  const rate = checkRateLimit(rateKey, ANSWERS_VERIFY_LIMIT);
  if (!rate.allowed) {
    return NextResponse.json({ error: t("facility.rateLimited") }, { status: 429 });
  }

  const profile = await getFacilityProfileRecoveryByPinHash(session.facilityId, pinHash);

  if (!profile) {
    return NextResponse.json({ error: t("facility.resetPinInvalid") }, { status: 403 });
  }

  const answer1Hash = hashRecoveryAnswer(answer1);
  const answer2Hash = hashRecoveryAnswer(answer2);

  if (
    !secureCompareHex(answer1Hash, profile.recovery_answer_1_hash) ||
    !secureCompareHex(answer2Hash, profile.recovery_answer_2_hash)
  ) {
    return NextResponse.json({ error: t("facility.resetAnswersWrong") }, { status: 403 });
  }

  const cookieStore = await cookies();
  cookieStore.set(
    FACILITY_RESET_COOKIE,
    serializeFacilityReset(buildFacilityResetData(session.facilityId, pinHash)),
    facilityResetCookieOptions()
  );

  return NextResponse.json({ success: true });
}
