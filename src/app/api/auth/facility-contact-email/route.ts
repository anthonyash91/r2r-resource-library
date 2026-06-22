import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
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

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: t("saved.email.signInRequired") }, { status: 401 });
  }

  const { data: profile } = await supabase
    .from("profiles")
    .select("signup_context")
    .eq("id", user.id)
    .maybeSingle();

  if (profile?.signup_context !== "facility") {
    return NextResponse.json({ error: t("facility.contactEmailNotAllowed") }, { status: 403 });
  }

  let body: { contactEmail?: string } = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const contactEmail = body.contactEmail?.trim() ?? "";
  if (!contactEmail || !isValidEmail(contactEmail)) {
    return NextResponse.json({ error: t("facility.contactEmailInvalid") }, { status: 400 });
  }

  const { error } = await supabase
    .from("profiles")
    .update({ contact_email: contactEmail })
    .eq("id", user.id);

  if (error) {
    return NextResponse.json({ error: t("facility.contactEmailSaveFailed") }, { status: 500 });
  }

  return NextResponse.json({ success: true, contactEmail });
}
