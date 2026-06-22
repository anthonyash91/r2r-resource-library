import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import {
  encryptSiteId,
  hashSiteId,
} from "@/lib/facility/crypto";
import { listFacilitiesWithCounts } from "@/lib/facility/data";
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
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  const facilities = await listFacilitiesWithCounts(supabase);
  return NextResponse.json({ facilities });
}

export async function POST(request: Request) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("admin.facilitiesUnavailable") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  let body: { name?: string; siteId?: string } = {};
  try {
    body = (await request.json()) as { name?: string; siteId?: string };
  } catch {
    body = {};
  }

  const name = body.name?.trim() ?? "";
  const siteId = body.siteId?.trim() ?? "";

  if (!name || !siteId) {
    return NextResponse.json({ error: t("admin.facilitySaveFailed") }, { status: 400 });
  }

  const siteIdHash = hashSiteId(siteId);

  const { data: existing } = await supabase
    .from("facilities")
    .select("id")
    .eq("site_id_hash", siteIdHash)
    .maybeSingle();

  if (existing) {
    return NextResponse.json({ error: t("admin.facilitySiteIdExists") }, { status: 409 });
  }

  const { data, error } = await supabase
    .from("facilities")
    .insert({
      name,
      site_id_hash: siteIdHash,
      site_id_encrypted: encryptSiteId(siteId),
      is_active: true,
    })
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
      signupCount: 0,
      siteId,
    },
  });
}
