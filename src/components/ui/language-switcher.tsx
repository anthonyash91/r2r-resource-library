"use client";

import { Globe } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  HEADER_INTERACTIVE_TRANSITION,
  headerControlSizeClass,
} from "@/components/layout/header-control-styles";
import { useTranslations } from "@/i18n/locale-context";
import type { Locale } from "@/i18n/types";

export function LanguageSwitcher({
  className,
  compact = false,
}: {
  className?: string;
  compact?: boolean;
}) {
  const { locale, setLocale, t } = useTranslations();

  const nextLocale: Locale = locale === "en" ? "es" : "en";
  const localeCode = locale === "en" ? "EN" : "ES";
  const nextLocaleLabel = nextLocale === "en" ? t("common.english") : t("common.spanish");

  return (
    <button
      type="button"
      onClick={() => setLocale(nextLocale)}
      className={cn(
        "inline-flex cursor-pointer items-center justify-center gap-2 rounded-xl border border-border bg-card font-semibold text-foreground",
        HEADER_INTERACTIVE_TRANSITION,
        headerControlSizeClass(compact),
        "hover:bg-muted focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
        className
      )}
      aria-label={`${t("common.language")}: ${localeCode}. ${t("common.switchTo")} ${nextLocaleLabel}`}
    >
      <Globe className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
      <span>{localeCode}</span>
    </button>
  );
}
