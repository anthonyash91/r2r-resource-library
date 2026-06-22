import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import { getFacilitySiteIdForAdmin } from "@/lib/facility/data";
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

export async function GET(_request: Request, context: RouteContext) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);
  const { id } = await context.params;

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  const siteId = await getFacilitySiteIdForAdmin(id, supabase);
  if (!siteId) {
    return NextResponse.json({ error: t("admin.facilityNotFound") }, { status: 404 });
  }

  return NextResponse.json({ siteId });
}

export async function PATCH(request: Request, context: RouteContext) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);
  const { id } = await context.params;

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  let body: { name?: string; isActive?: boolean } = {};
  try {
    body = (await request.json()) as { name?: string; isActive?: boolean };
  } catch {
    body = {};
  }

  const update: { name?: string; is_active?: boolean } = {};
  if (typeof body.name === "string" && body.name.trim()) {
    update.name = body.name.trim();
  }
  if (typeof body.isActive === "boolean") {
    update.is_active = body.isActive;
  }

  if (!Object.keys(update).length) {
    return NextResponse.json({ error: t("admin.facilitySaveFailed") }, { status: 400 });
  }

  const { data, error } = await supabase
    .from("facilities")
    .update(update)
    .eq("id", id)
    .select("id, name, is_active, created_at, updated_at")
    .single();

  if (error || !data) {
    return NextResponse.json({ error: t("admin.facilitySaveFailed") }, { status: 500 });
  }

  return NextResponse.json({
    facility: {
      id: data.id,
      name: data.name,
      isActive: data.is_active,
      createdAt: data.created_at,
      updatedAt: data.updated_at,
    },
  });
}
