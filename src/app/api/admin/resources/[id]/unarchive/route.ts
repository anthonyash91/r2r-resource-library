import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import { unarchiveResourceByIdServer } from "@/lib/admin-resources-server";
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

export async function POST(_request: Request, context: RouteContext) {
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

  const result = await unarchiveResourceByIdServer(id);
  if (result.error) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 500 });
  }

  return NextResponse.json({ success: true });
}
