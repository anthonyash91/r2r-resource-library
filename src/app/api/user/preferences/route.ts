import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";
import {
  profileUpdateFromPreferences,
  validatePreferencesInput,
} from "@/lib/user-preferences/parse";
import type { UserPreferencesInput } from "@/lib/user-preferences/types";
import { cookies } from "next/headers";

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

  let body: UserPreferencesInput = {
    state: "",
    county: "",
    priorityCategories: [],
  };

  try {
    body = (await request.json()) as UserPreferencesInput;
  } catch {
    return NextResponse.json({ error: t("onboarding.saveFailed") }, { status: 400 });
  }

  const prefs = validatePreferencesInput(body);
  if (!prefs) {
    return NextResponse.json({ error: t("onboarding.saveFailed") }, { status: 400 });
  }

  const admin = createAdminClient();
  const db = admin ?? supabase;
  const { error } = await db
    .from("profiles")
    .update(profileUpdateFromPreferences(prefs))
    .eq("id", user.id);

  if (error) {
    return NextResponse.json({ error: t("onboarding.saveFailed") }, { status: 500 });
  }

  return NextResponse.json({ prefs });
}
