"use client";

import { Mail, Phone } from "lucide-react";
import { useTranslations } from "@/i18n/locale-context";

export function CrisisBar() {
  const { t } = useTranslations();

  return (
    <aside
      className="border-t border-border bg-muted text-foreground"
      aria-label={t("crisisBar.message")}
    >
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-4 py-4 sm:flex-row sm:px-6 lg:px-8">
        <p className="text-center text-base font-semibold sm:text-left sm:text-lg">
          {t("crisisBar.message")}
        </p>

        <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm font-medium sm:text-base">
          <a
            href="tel:988"
            className="inline-flex items-center gap-2 rounded-lg text-primary underline-offset-2 transition-colors hover:text-primary-hover hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            aria-label={t("crisisBar.call988Aria")}
          >
            <Phone className="h-4 w-4 shrink-0" aria-hidden="true" />
            {t("crisisBar.call988")}
          </a>
          <a
            href="sms:741741?body=HOME"
            className="inline-flex items-center gap-2 rounded-lg text-primary underline-offset-2 transition-colors hover:text-primary-hover hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            aria-label={t("crisisBar.textLineAria")}
          >
            <Mail className="h-4 w-4 shrink-0" aria-hidden="true" />
            {t("crisisBar.textLine")}
          </a>
        </div>
      </div>
    </aside>
  );
}
