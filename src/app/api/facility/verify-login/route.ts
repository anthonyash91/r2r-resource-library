import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { verifyFacilityProfileBinding } from "@/lib/facility/data";
import { readFacilitySession } from "@/lib/facility/session";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

export async function GET() {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const facilitySession = await readFacilitySession();
  if (!facilitySession) {
    return NextResponse.json({ facilityMode: false, valid: true });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ facilityMode: true, valid: true, authenticated: false });
  }

  const valid = await verifyFacilityProfileBinding(
    user.id,
    facilitySession.facilityId,
    facilitySession.pinHash
  );

  if (!valid) {
    return NextResponse.json({ facilityMode: true, valid: false }, { status: 403 });
  }

  return NextResponse.json({ facilityMode: true, valid: true, authenticated: true });
}
