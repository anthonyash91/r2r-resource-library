import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { isSupabaseConfigured } from "@/lib/supabase/server";
import { facilityAccountExistsByPinHash } from "@/lib/facility/data";
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

  const exists = await facilityAccountExistsByPinHash(session.facilityId, session.pinHash);
  if (exists) {
    return NextResponse.json({ error: t("facility.accountAlreadyExists") }, { status: 409 });
  }

  let body: {
    email?: string;
    password?: string;
    fullName?: string;
    recoveryQuestion1?: string;
    recoveryAnswer1?: string;
    recoveryQuestion2?: string;
    recoveryAnswer2?: string;
  } = {};

  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const email = body.email?.trim() ?? "";
  const password = body.password ?? "";
  const fullName = body.fullName?.trim() ?? "";
  const recoveryQuestion1 = body.recoveryQuestion1?.trim() ?? "";
  const recoveryAnswer1 = body.recoveryAnswer1?.trim() ?? "";
  const recoveryQuestion2 = body.recoveryQuestion2?.trim() ?? "";
  const recoveryAnswer2 = body.recoveryAnswer2?.trim() ?? "";

  if (
    !email ||
    !isValidEmail(email) ||
    password.length < 8 ||
    !fullName ||
    !recoveryQuestion1 ||
    !recoveryAnswer1 ||
    !recoveryQuestion2 ||
    !recoveryAnswer2
  ) {
    return NextResponse.json({ error: t("facility.signupInvalid") }, { status: 400 });
  }

  const { data: created, error: createError } = await admin.auth.admin.createUser({
    email,
    password,
    email_confirm: true,
    user_metadata: { full_name: fullName },
  });

  if (createError || !created.user) {
    return NextResponse.json({ error: t("auth.signUpFailed") }, { status: 400 });
  }

  const userId = created.user.id;

  const { error: profileError } = await admin
    .from("profiles")
    .update({
      full_name: fullName,
      signup_context: "facility",
      facility_id: session.facilityId,
      inmate_pin_hash: session.pinHash,
      recovery_question_1: recoveryQuestion1,
      recovery_answer_1_hash: hashRecoveryAnswer(recoveryAnswer1),
      recovery_question_2: recoveryQuestion2,
      recovery_answer_2_hash: hashRecoveryAnswer(recoveryAnswer2),
    })
    .eq("id", userId);

  if (profileError) {
    await admin.auth.admin.deleteUser(userId);
    return NextResponse.json({ error: t("auth.signUpFailed") }, { status: 500 });
  }

  return NextResponse.json({ success: true, userId });
}
