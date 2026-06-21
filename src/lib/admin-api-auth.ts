import { NextResponse } from "next/server";
import type { SupabaseClient } from "@supabase/supabase-js";
import { createTranslator } from "@/i18n/translator";
import type { Locale } from "@/i18n/types";
import { getAdminSession } from "@/lib/admin-auth";

export async function requireAdminApiAccess(
  supabase: SupabaseClient,
  locale: Locale
): Promise<{ userId: string } | NextResponse> {
  const { t } = createTranslator(locale);

  const session = await getAdminSession(supabase);
  if (!session) {
    return NextResponse.json({ error: t("admin.accessRequired") }, { status: 401 });
  }

  return session;
}
