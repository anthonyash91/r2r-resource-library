"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTranslations } from "@/i18n/locale-context";
import { shouldShowOnboardingPrompt, readClientPreferences } from "@/lib/user-preferences";
import { PREFS_UPDATED_EVENT } from "@/components/facility/facility-session-preferences-hydration";

const DISMISS_KEY = "reentry_onboarding_banner_dismissed";

export function OnboardingPromptBanner() {
  const { t } = useTranslations();
  const pathname = usePathname();
  const [dismissed, setDismissed] = useState(false);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const refresh = () => {
      setDismissed(sessionStorage.getItem(DISMISS_KEY) === "1");
      setShowPrompt(shouldShowOnboardingPrompt(readClientPreferences()));
    };

    refresh();
    window.addEventListener(PREFS_UPDATED_EVENT, refresh);
    return () => window.removeEventListener(PREFS_UPDATED_EVENT, refresh);
  }, [pathname]);

  const dismiss = () => {
    sessionStorage.setItem(DISMISS_KEY, "1");
    setDismissed(true);
  };

  const visible = !dismissed && showPrompt;

  if (!visible) return null;

  return (
    <div className="relative border-b border-primary/20 bg-secondary/80 px-4 py-4 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="pr-8 sm:pr-0">
          <p className="text-base font-semibold text-foreground">{t("onboarding.bannerTitle")}</p>
          <p className="mt-1 text-sm text-muted-foreground">{t("onboarding.bannerDesc")}</p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Link href="/get-started">
            <Button size="sm">{t("onboarding.bannerCta")}</Button>
          </Link>
          <Button type="button" variant="ghost" size="sm" onClick={dismiss}>
            {t("onboarding.bannerDismiss")}
          </Button>
        </div>
        <button
          type="button"
          onClick={dismiss}
          className="absolute right-3 top-3 rounded-lg p-2 text-muted-foreground hover:bg-muted sm:hidden"
          aria-label={t("onboarding.bannerDismiss")}
        >
          <X className="h-5 w-5" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}
