import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { getFacilityProfileByPinHash } from "@/lib/facility/data";
import { readFacilitySession } from "@/lib/facility/session";
import { formatAuthError } from "@/lib/auth-errors";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";
import { PREFS_COOKIE } from "@/lib/user-preferences/constants";
import { applyCookiePreferencesToProfileIfNeeded } from "@/lib/user-preferences/apply-cookie-to-profile";

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

  const session = await readFacilitySession();
  if (!session) {
    return NextResponse.json({ error: t("facility.sessionRequired") }, { status: 401 });
  }

  let body: { password?: string } = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const password = body.password ?? "";
  if (password.length < 8) {
    return NextResponse.json({ error: t("facility.loginInvalid") }, { status: 400 });
  }

  const profile = await getFacilityProfileByPinHash(session.facilityId, session.pinHash);
  if (!profile) {
    return NextResponse.json({ error: t("facility.noAccountDesc") }, { status: 404 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const { error } = await supabase.auth.signInWithPassword({
    email: profile.email,
    password,
  });

  if (error) {
    return NextResponse.json(
      { error: formatAuthError(error, t("auth.signInFailed")) },
      { status: 401 }
    );
  }

  const cookieStore = await cookies();
  await applyCookiePreferencesToProfileIfNeeded(
    supabase,
    profile.id,
    cookieStore.get(PREFS_COOKIE)?.value
  );

  return NextResponse.json({ success: true });
}
