import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import { hashRecoveryAnswer } from "@/lib/facility/crypto";
import { readFacilitySession } from "@/lib/facility/session";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
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

  let body: {
    email?: string;
    password?: string;
    answer1?: string;
    answer2?: string;
  } = {};

  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const email = body.email?.trim() ?? "";
  const password = body.password ?? "";
  const answer1 = body.answer1 ?? "";
  const answer2 = body.answer2 ?? "";

  if (!email || !isValidEmail(email) || password.length < 8 || !answer1 || !answer2) {
    return NextResponse.json({ error: t("facility.resetInvalid") }, { status: 400 });
  }

  const { data: profile, error: profileError } = await admin
    .from("profiles")
    .select(
      "id, email, signup_context, facility_id, inmate_pin_hash, recovery_answer_1_hash, recovery_answer_2_hash"
    )
    .eq("email", email)
    .eq("signup_context", "facility")
    .eq("facility_id", session.facilityId)
    .eq("inmate_pin_hash", session.pinHash)
    .maybeSingle();

  if (profileError || !profile) {
    return NextResponse.json({ error: t("facility.resetFailed") }, { status: 400 });
  }

  const answer1Hash = hashRecoveryAnswer(answer1);
  const answer2Hash = hashRecoveryAnswer(answer2);

  if (
    answer1Hash !== profile.recovery_answer_1_hash ||
    answer2Hash !== profile.recovery_answer_2_hash
  ) {
    return NextResponse.json({ error: t("facility.resetAnswersWrong") }, { status: 403 });
  }

  const { error: updateError } = await admin.auth.admin.updateUserById(profile.id, {
    password,
  });

  if (updateError) {
    return NextResponse.json({ error: t("facility.resetFailed") }, { status: 500 });
  }

  return NextResponse.json({ success: true });
}
