import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import { isTranslationConfigured, translateTextsToSpanish } from "@/lib/translation/deepl";
import {
  EDITABLE_ABOUT_CONTENT_FIELDS,
  type AboutContentFormValues,
} from "@/lib/about-content-fields";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

function normalizePayload(body: unknown): AboutContentFormValues | null {
  if (!body || typeof body !== "object") return null;

  const record = body as Record<string, unknown>;
  const payload = {} as AboutContentFormValues;

  for (const field of EDITABLE_ABOUT_CONTENT_FIELDS) {
    if (typeof record[field] !== "string") return null;
    payload[field] = record[field].trim();
  }

  return payload;
}

export async function POST(request: Request) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("admin.aboutSaveFailed") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.aboutSaveFailed") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  const payload = normalizePayload(await request.json());
  if (!payload) {
    return NextResponse.json({ error: t("admin.aboutSaveFailed") }, { status: 400 });
  }

  let spanish: string[] = [];
  let translated = false;

  if (isTranslationConfigured()) {
    try {
      spanish = await translateTextsToSpanish(
        EDITABLE_ABOUT_CONTENT_FIELDS.map((field) => payload[field])
      );
      translated = true;
    } catch (error) {
      console.error("About page translation failed:", error);
      return NextResponse.json({ error: t("admin.translationFailed") }, { status: 502 });
    }
  }

  const entries: { key: string; value: string }[] = EDITABLE_ABOUT_CONTENT_FIELDS.map((field) => ({
    key: field,
    value: payload[field],
  }));

  if (translated) {
    EDITABLE_ABOUT_CONTENT_FIELDS.forEach((field, index) => {
      entries.push({
        key: `${field}_es`,
        value: spanish[index] ?? "",
      });
    });
  }

  for (const entry of entries) {
    const { error } = await supabase
      .from("homepage_content")
      .upsert(entry, { onConflict: "key" });

    if (error) {
      console.error("About content save failed:", error);
      return NextResponse.json({ error: t("admin.aboutSaveFailed") }, { status: 500 });
    }
  }

  return NextResponse.json({
    success: true,
    translated,
  });
}
