import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createAdminClient } from "@/lib/supabase/admin";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { requireAdminApiAccess } from "@/lib/api-auth";
import { deleteUserAccount } from "@/lib/admin/delete-user";
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

export async function DELETE(_request: Request, context: RouteContext) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);
  const { id: targetUserId } = await context.params;

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("auth.authUnavailable") }, { status: 503 });
  }

  const authResult = await requireAdminApiAccess(supabase, locale);
  if (authResult instanceof NextResponse) return authResult;

  if (targetUserId === authResult.userId) {
    return NextResponse.json({ error: t("admin.cannotDeleteSelf") }, { status: 403 });
  }

  const admin = createAdminClient();
  if (!admin) {
    return NextResponse.json({ error: t("admin.userDeleteUnavailable") }, { status: 503 });
  }

  const { data: profile, error: profileError } = await admin
    .from("profiles")
    .select("id, role, full_name, email")
    .eq("id", targetUserId)
    .maybeSingle();

  if (profileError || !profile) {
    return NextResponse.json({ error: t("admin.userNotFound") }, { status: 404 });
  }

  if (profile.role === "admin") {
    return NextResponse.json({ error: t("admin.cannotDeleteAdmin") }, { status: 403 });
  }

  const result = await deleteUserAccount(admin, targetUserId);
  if (!result.success) {
    if (process.env.NODE_ENV === "development") {
      console.error("[admin delete user]", targetUserId, result.error);
    }

    const body: { error: string; detail?: string } = { error: t("admin.deleteUserFailed") };
    if (process.env.NODE_ENV === "development" && result.error) {
      body.detail = result.error;
    }

    return NextResponse.json(body, { status: 500 });
  }

  return NextResponse.json({ success: true });
}
