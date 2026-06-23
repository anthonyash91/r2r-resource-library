import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { facilityAccountExistsByPinHash } from "@/lib/facility/data";
import { buildFacilityAuthEmail } from "@/lib/facility/auth-email";
import { hashRecoveryAnswer } from "@/lib/facility/crypto";
import { isFacilityPasswordValid } from "@/lib/facility/password-policy";
import { readFacilitySession } from "@/lib/facility/session";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";
import { PREFS_COOKIE } from "@/lib/user-preferences/constants";
import { profilePreferenceFieldsFromCookie } from "@/lib/user-preferences/apply-cookie-to-profile";

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

  const contactEmail = body.email?.trim() ?? "";
  const password = body.password ?? "";
  const fullName = body.fullName?.trim() ?? "";
  const recoveryQuestion1 = body.recoveryQuestion1?.trim() ?? "";
  const recoveryAnswer1 = body.recoveryAnswer1?.trim() ?? "";
  const recoveryQuestion2 = body.recoveryQuestion2?.trim() ?? "";
  const recoveryAnswer2 = body.recoveryAnswer2?.trim() ?? "";

  if (
    !isFacilityPasswordValid(password) ||
    !fullName ||
    !recoveryQuestion1 ||
    !recoveryAnswer1 ||
    !recoveryQuestion2 ||
    !recoveryAnswer2
  ) {
    return NextResponse.json({ error: t("facility.signupInvalid") }, { status: 400 });
  }

  if (contactEmail && !isValidEmail(contactEmail)) {
    return NextResponse.json({ error: t("facility.signupInvalid") }, { status: 400 });
  }

  const authEmail = buildFacilityAuthEmail(session.facilityId, session.pinHash);

  const { data: created, error: createError } = await admin.auth.admin.createUser({
    email: authEmail,
    password,
    email_confirm: true,
    user_metadata: { full_name: fullName },
  });

  if (createError || !created.user) {
    return NextResponse.json({ error: t("auth.signUpFailed") }, { status: 400 });
  }

  const userId = created.user.id;

  const cookieStore = await cookies();
  const preferenceFields = profilePreferenceFieldsFromCookie(
    cookieStore.get(PREFS_COOKIE)?.value
  );

  const { error: profileError } = await admin
    .from("profiles")
    .update({
      full_name: fullName,
      email: authEmail,
      contact_email: contactEmail || null,
      signup_context: "facility",
      facility_id: session.facilityId,
      inmate_pin_hash: session.pinHash,
      recovery_question_1: recoveryQuestion1,
      recovery_answer_1_hash: hashRecoveryAnswer(recoveryAnswer1),
      recovery_question_2: recoveryQuestion2,
      recovery_answer_2_hash: hashRecoveryAnswer(recoveryAnswer2),
      ...(preferenceFields ?? {}),
    })
    .eq("id", userId);

  if (profileError) {
    await admin.auth.admin.deleteUser(userId);
    return NextResponse.json({ error: t("auth.signUpFailed") }, { status: 500 });
  }

  const supabase = await createClient();
  if (supabase) {
    await supabase.auth.signInWithPassword({ email: authEmail, password });
  }

  const response = NextResponse.json({ success: true, userId });
  return response;
}
