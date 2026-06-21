import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { getSavedResourcesForUser, getSiteBranding } from "@/lib/data";
import {
  generateSavedResourcesPdf,
  getSavedResourcesPdfLabels,
} from "@/lib/pdf/saved-resources-pdf";
import { getSavedResourcesPdfBranding } from "@/lib/pdf/pdf-branding";
import { isEmailConfigured, sendSavedResourcesPdfEmail } from "@/lib/email/send-saved-resources-pdf";
import {
  getSavedPdfEmailStatus,
  isAdminPdfEmailUnlimited,
  SAVED_PDF_EMAIL_LIMIT,
} from "@/lib/saved-pdf-email";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

async function getAuthenticatedProfile(supabase: NonNullable<Awaited<ReturnType<typeof createClient>>>) {
  const {
    data: { user: authUser },
    error: authError,
  } = await supabase.auth.getUser();

  if (authError || !authUser) {
    return { error: "signInRequired" as const };
  }

  const { data: profile, error: profileError } = await supabase
    .from("profiles")
    .select("email, full_name, saved_pdf_emails_sent, role")
    .eq("id", authUser.id)
    .single();

  if (profileError) {
    return { error: "failed" as const };
  }

  return { authUser, profile };
}

export async function GET() {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("saved.email.unavailable") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("saved.email.unavailable") }, { status: 503 });
  }

  const result = await getAuthenticatedProfile(supabase);
  if ("error" in result) {
    if (result.error === "signInRequired") {
      return NextResponse.json({ error: t("saved.email.signInRequired") }, { status: 401 });
    }
    return NextResponse.json({ error: t("saved.email.failed") }, { status: 400 });
  }

  const unlimited = isAdminPdfEmailUnlimited(result.profile.role);
  const status = getSavedPdfEmailStatus(result.profile.saved_pdf_emails_sent ?? 0, { unlimited });
  return NextResponse.json(status);
}

export async function POST(request: Request) {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);

  if (!isSupabaseConfigured()) {
    return NextResponse.json({ error: t("saved.email.unavailable") }, { status: 503 });
  }

  if (!isEmailConfigured()) {
    return NextResponse.json({ error: t("saved.email.notConfigured") }, { status: 503 });
  }

  const supabase = await createClient();
  if (!supabase) {
    return NextResponse.json({ error: t("saved.email.unavailable") }, { status: 503 });
  }

  const authResult = await getAuthenticatedProfile(supabase);
  if ("error" in authResult) {
    if (authResult.error === "signInRequired") {
      return NextResponse.json({ error: t("saved.email.signInRequired") }, { status: 401 });
    }
    return NextResponse.json({ error: t("saved.email.failed") }, { status: 400 });
  }

  const { authUser, profile } = authResult;
  const unlimited = isAdminPdfEmailUnlimited(profile.role);
  const currentStatus = getSavedPdfEmailStatus(profile.saved_pdf_emails_sent ?? 0, { unlimited });

  if (!unlimited && currentStatus.remaining === 0) {
    return NextResponse.json(
      {
        error: t("saved.email.limitReached", { limit: SAVED_PDF_EMAIL_LIMIT }),
        ...currentStatus,
      },
      { status: 429 }
    );
  }

  let body: { email?: string } = {};
  try {
    body = (await request.json()) as { email?: string };
  } catch {
    body = {};
  }

  const recipientEmail = body.email?.trim() ?? "";
  if (!recipientEmail || !isValidEmail(recipientEmail)) {
    return NextResponse.json({ error: t("saved.email.invalidEmail") }, { status: 400 });
  }

  const resources = await getSavedResourcesForUser(authUser.id, locale);

  if (resources.length === 0) {
    return NextResponse.json({ error: t("saved.email.empty") }, { status: 400 });
  }

  let reservedCount: number | null = profile.saved_pdf_emails_sent ?? 0;

  if (!unlimited) {
    const { data: incrementedCount, error: reserveError } = await supabase.rpc(
      "increment_saved_pdf_email_send",
      { p_limit: SAVED_PDF_EMAIL_LIMIT }
    );

    if (reserveError || incrementedCount == null) {
      const status = getSavedPdfEmailStatus(profile.saved_pdf_emails_sent ?? 0);
      return NextResponse.json(
        {
          error: t("saved.email.limitReached", { limit: SAVED_PDF_EMAIL_LIMIT }),
          ...status,
        },
        { status: 429 }
      );
    }

    reservedCount = incrementedCount;
  }

  try {
    const [labels, siteBranding] = await Promise.all([
      getSavedResourcesPdfLabels(locale),
      getSiteBranding(),
    ]);
    const pdf = await generateSavedResourcesPdf({
      resources,
      labels,
      locale,
      recipientName: profile?.full_name,
      branding: getSavedResourcesPdfBranding(locale, siteBranding),
    });

    await sendSavedResourcesPdfEmail({
      to: recipientEmail,
      recipientName: profile?.full_name,
      pdf,
      resourceCount: resources.length,
      locale,
    });

    const status = getSavedPdfEmailStatus(reservedCount ?? 0, { unlimited });
    return NextResponse.json({
      success: true,
      email: recipientEmail,
      count: resources.length,
      ...status,
    });
  } catch (error) {
    if (!unlimited) {
      await supabase.rpc("decrement_saved_pdf_email_send");
    }
    console.error("Failed to email saved resources PDF:", error);
    return NextResponse.json({ error: t("saved.email.failed") }, { status: 500 });
  }
}
