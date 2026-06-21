import { Resend } from "resend";
import type { Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

export function isEmailConfigured(): boolean {
  return Boolean(process.env.RESEND_API_KEY && process.env.EMAIL_FROM);
}

export async function sendSavedResourcesPdfEmail(options: {
  to: string;
  recipientName?: string | null;
  pdf: Buffer;
  resourceCount: number;
  locale: Locale;
}): Promise<void> {
  if (!isEmailConfigured()) {
    throw new Error("EMAIL_NOT_CONFIGURED");
  }

  const apiKey = process.env.RESEND_API_KEY!;
  const from = process.env.EMAIL_FROM!;
  const { t } = createTranslator(options.locale);
  const subject = t("saved.email.subject", { count: options.resourceCount });
  const filename = t("saved.email.filename");
  const greeting = options.recipientName?.trim()
    ? t("saved.email.greetingNamed", { name: options.recipientName.trim() })
    : t("saved.email.greeting");
  const body = t("saved.email.body", { count: options.resourceCount });

  const resend = new Resend(apiKey);
  const { error } = await resend.emails.send({
    from,
    to: options.to,
    subject,
    text: `${greeting}\n\n${body}`,
    attachments: [
      {
        filename,
        content: options.pdf.toString("base64"),
      },
    ],
  });

  if (error) {
    throw new Error(error.message);
  }
}
