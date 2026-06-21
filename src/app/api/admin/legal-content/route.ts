import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/admin-api-auth";
import { isTranslationConfigured, translateTextsToSpanish } from "@/lib/translation/deepl";
import {
  EDITABLE_ACCESSIBILITY_CONTENT_FIELDS,
  type LegalDocumentSlug,
} from "@/lib/legal-content-fields";
import { getEditableFieldsForLegalDocument } from "@/lib/legal-content";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

type LegalSaveDocument = LegalDocumentSlug | "accessibility";

function getFieldsForDocument(document: LegalSaveDocument): readonly string[] {
  if (document === "accessibility") return EDITABLE_ACCESSIBILITY_CONTENT_FIELDS;
  return getEditableFieldsForLegalDocument(document);
}

function normalizePayload(
  body: unknown,
  fields: readonly string[]
): Record<string, string> | null {
  if (!body || typeof body !== "object") return null;

  const record = body as Record<string, unknown>;
  const payload: Record<string, string> = {};

  for (const field of fields) {
    if (typeof record[field] !== "string") return null;
    payload[field] = record[field].trim();
  }

  return payload;
}

export async function POST(request: Request) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("admin.legalSaveFailed") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.legalSaveFailed") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  const body = (await request.json()) as { document?: string; content?: unknown };
  const document = body.document as LegalSaveDocument | undefined;

  if (!document || !["privacy", "terms", "accessibility"].includes(document)) {
    return NextResponse.json({ error: t("admin.legalSaveFailed") }, { status: 400 });
  }

  const fields = getFieldsForDocument(document);
  const payload = normalizePayload(body.content, fields);

  if (!payload) {
    return NextResponse.json({ error: t("admin.legalSaveFailed") }, { status: 400 });
  }

  let spanish: string[] = [];
  let translated = false;

  if (isTranslationConfigured()) {
    try {
      spanish = await translateTextsToSpanish(fields.map((field) => payload[field]));
      translated = true;
    } catch (error) {
      console.error("Legal content translation failed:", error);
      return NextResponse.json({ error: t("admin.translationFailed") }, { status: 502 });
    }
  }

  const entries: { key: string; value: string }[] = fields.map((field) => ({
    key: field,
    value: payload[field],
  }));

  if (translated) {
    fields.forEach((field, index) => {
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
      console.error("Legal content save failed:", error);
      return NextResponse.json({ error: t("admin.legalSaveFailed") }, { status: 500 });
    }
  }

  return NextResponse.json({
    success: true,
    translated,
  });
}
