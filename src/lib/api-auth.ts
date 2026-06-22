import { NextResponse, type NextRequest } from "next/server";
import type { SupabaseClient, User } from "@supabase/supabase-js";
import { createTranslator } from "@/i18n/translator";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { getAdminSession } from "@/lib/admin-auth";

export function getRequestLocaleFromRequest(request: NextRequest): Locale {
  const value = request.cookies.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

export async function requireAuthenticatedApiAccess(
  supabase: SupabaseClient,
  locale: Locale
): Promise<{ userId: string; user: User } | NextResponse> {
  const { t } = createTranslator(locale);

  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) {
    return NextResponse.json({ error: t("saved.email.signInRequired") }, { status: 401 });
  }

  return { userId: user.id, user };
}

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

/** Middleware gate: admin auth, user auth, or 404 for unknown API paths. */
export async function enforceApiRouteAccess(
  request: NextRequest,
  supabase: SupabaseClient
): Promise<NextResponse | null> {
  const pathname = request.nextUrl.pathname;
  if (!pathname.startsWith("/api/")) {
    return null;
  }

  const locale = getRequestLocaleFromRequest(request);

  if (pathname.startsWith("/api/admin")) {
    const authResult = await requireAdminApiAccess(supabase, locale);
    if (authResult instanceof NextResponse) {
      return authResult;
    }
    return null;
  }

  if (pathname.startsWith("/api/saved-resources")) {
    const authResult = await requireAuthenticatedApiAccess(supabase, locale);
    if (authResult instanceof NextResponse) {
      return authResult;
    }
    return null;
  }

  if (
    pathname.startsWith("/api/auth/facility-signup") ||
    pathname.startsWith("/api/auth/facility-reset-password") ||
    pathname.startsWith("/api/facility/")
  ) {
    return null;
  }

  return NextResponse.json({ error: "Not found" }, { status: 404 });
}
