"use client";

import { useTranslations } from "@/i18n/locale-context";
import type { Locale } from "@/i18n/types";

const footerLinkClass =
  "block text-[13px] leading-none text-[var(--footer-muted)] transition-colors hover:text-[var(--footer-foreground)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--footer-accent)] rounded";

export function FooterLocaleLink() {
  const { locale, setLocale, t } = useTranslations();
  const nextLocale: Locale = locale === "en" ? "es" : "en";
  const label = nextLocale === "es" ? t("common.spanish") : t("common.english");

  return (
    <button
      type="button"
      onClick={() => setLocale(nextLocale)}
      className={footerLinkClass}
      aria-label={`${t("common.language")}: ${t("common.switchTo")} ${label}`}
    >
      {label}
    </button>
  );
}
