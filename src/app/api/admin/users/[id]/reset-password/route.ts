import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import { buildFacilityAuthEmail } from "@/lib/facility/auth-email";
import { hashInmatePin, normalizePin } from "@/lib/facility/crypto";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

interface RouteContext {
  params: Promise<{ id: string }>;
}

export async function POST(request: Request, context: RouteContext) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);
  const { id: targetUserId } = await context.params;

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  const admin = createAdminClient();
  if (!admin) {
    return NextResponse.json({ error: t("admin.userDeleteUnavailable") }, { status: 503 });
  }

  let body: { pin?: string; password?: string } = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const pin = normalizePin(body.pin ?? "");
  const password = body.password ?? "";

  if (!pin || password.length < 8) {
    return NextResponse.json({ error: t("admin.resetPinInvalid") }, { status: 400 });
  }

  const { data: profile, error: profileError } = await admin
    .from("profiles")
    .select("id, signup_context, facility_id, inmate_pin_hash")
    .eq("id", targetUserId)
    .maybeSingle();

  if (profileError || !profile) {
    return NextResponse.json({ error: t("admin.userNotFound") }, { status: 404 });
  }

  if (profile.signup_context !== "facility" || !profile.facility_id) {
    return NextResponse.json({ error: t("admin.resetPinUnavailable") }, { status: 400 });
  }

  const facilityId = profile.facility_id;
  const newPinHash = hashInmatePin(facilityId, pin);

  if (newPinHash !== profile.inmate_pin_hash) {
    const { data: conflict, error: conflictError } = await admin
      .from("profiles")
      .select("id")
      .eq("facility_id", facilityId)
      .eq("inmate_pin_hash", newPinHash)
      .eq("signup_context", "facility")
      .neq("id", targetUserId)
      .maybeSingle();

    if (conflictError) {
      return NextResponse.json({ error: t("admin.resetPinFailed") }, { status: 500 });
    }

    if (conflict) {
      return NextResponse.json({ error: t("admin.resetPinConflict") }, { status: 409 });
    }
  }

  const authEmail = buildFacilityAuthEmail(facilityId, pin);

  const { error: authError } = await admin.auth.admin.updateUserById(targetUserId, {
    email: authEmail,
    password,
    email_confirm: true,
  });

  if (authError) {
    return NextResponse.json({ error: t("admin.resetPinFailed") }, { status: 500 });
  }

  const { error: updateError } = await admin
    .from("profiles")
    .update({
      email: authEmail,
      inmate_pin_hash: newPinHash,
    })
    .eq("id", targetUserId);

  if (updateError) {
    return NextResponse.json({ error: t("admin.resetPinFailed") }, { status: 500 });
  }

  return NextResponse.json({ success: true });
}
