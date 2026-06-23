import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import { createResourceServer } from "@/lib/admin-resources-server";
import type { ResourceFormData } from "@/lib/admin-resources";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

export async function POST(request: Request) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  let form: ResourceFormData;
  try {
    form = (await request.json()) as ResourceFormData;
  } catch {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 400 });
  }

  const result = await createResourceServer(form);
  if (result.error === "max_featured") {
    return NextResponse.json({ error: "max_featured" }, { status: 409 });
  }
  if (result.error) {
    return NextResponse.json({ error: t("admin.resourceSaveFailed") }, { status: 500 });
  }

  return NextResponse.json({ id: result.id });
}
