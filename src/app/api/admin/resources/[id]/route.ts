import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import { updateResourceServer } from "@/lib/admin-resources-server";
import type { ResourceFormData } from "@/lib/admin-resources";
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

export async function PATCH(request: Request, context: RouteContext) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);
  const { id } = await context.params;

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  let body: { form?: ResourceFormData; wasFeatured?: boolean } = {};
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 400 });
  }

  if (!body.form) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 400 });
  }

  const result = await updateResourceServer(id, body.form, body.wasFeatured ?? false);
  if (result.error === "max_featured") {
    return NextResponse.json({ error: "max_featured" }, { status: 409 });
  }
  if (result.error) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 500 });
  }

  return NextResponse.json({ success: true });
}
