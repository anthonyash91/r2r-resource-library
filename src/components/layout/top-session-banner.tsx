"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";
import { useFacilityTabletStatus } from "@/hooks/use-facility-tablet-status";
import { shouldShowOnboardingPrompt, readClientPreferences } from "@/lib/user-preferences";
import { PREFS_UPDATED_EVENT } from "@/components/facility/facility-session-preferences-hydration";
import { cn } from "@/lib/utils";

const DISMISS_KEY = "reentry_onboarding_banner_dismissed";

const bannerShellClass =
  "border-b border-border bg-[var(--soft)] px-4 py-2.5 sm:px-9";

const onboardingCtaClass =
  "inline-flex h-auto min-h-0 items-center justify-center rounded-[9px] bg-[var(--coral)] px-3.5 py-1.5 font-heading text-[13px] font-bold leading-none text-white transition-colors hover:bg-[var(--coral-hover)] focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2";

const onboardingDismissClass =
  "inline-flex h-auto min-h-0 cursor-pointer items-center justify-center rounded-[9px] px-2 py-1.5 font-heading text-[13px] font-semibold leading-none text-muted-foreground transition-colors hover:text-foreground focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2";

function FacilitySessionBanner({ hasAccount }: { hasAccount: boolean }) {
  const { t } = useTranslations();

  return (
    <div className={bannerShellClass}>
      <div
        className={cn(
          "mx-auto max-w-7xl",
          !hasAccount && "flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
        )}
      >
        {hasAccount ? (
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-base font-semibold text-foreground">
              {t("facility.barSignInTitle")}
            </p>
            <p className="mt-1 text-base text-foreground">{t("facility.barSignInDesc")}</p>
            <div className="mt-4">
              <Link href="/facility/login">
                <Button size="sm">{t("auth.signIn")}</Button>
              </Link>
            </div>
          </div>
        ) : (
          <>
            <div>
              <p className="text-base font-semibold text-foreground">{t("facility.barTitle")}</p>
              <p className="mt-1 text-sm text-muted-foreground">{t("facility.barDesc")}</p>
              <p className="mt-1 text-sm text-muted-foreground">{t("facility.privacyReminder")}</p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Link href="/facility/signup">
                <Button size="sm">{t("facility.createAccount")}</Button>
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function OnboardingPromptBannerContent({
  onDismiss,
}: {
  onDismiss: () => void;
}) {
  const { t } = useTranslations();

  return (
    <div className={cn(bannerShellClass, "relative")}>
      <div className="mx-auto flex max-w-[1180px] flex-col gap-2 sm:flex-row sm:items-center sm:justify-between sm:gap-4">
        <div className="min-w-0 pr-8 sm:pr-0">
          <p className="font-heading text-sm font-semibold leading-snug text-foreground">
            {t("onboarding.bannerTitle")}
          </p>
          <p className="mt-0.5 text-[13px] leading-snug text-muted-foreground">
            {t("onboarding.bannerDesc")}
          </p>
        </div>
        <div className="flex shrink-0 flex-wrap items-center gap-2">
          <Link href="/get-started" className={onboardingCtaClass}>
            {t("onboarding.bannerCta")}
          </Link>
          <button type="button" className={onboardingDismissClass} onClick={onDismiss}>
            {t("onboarding.bannerDismiss")}
          </button>
        </div>
        <button
          type="button"
          onClick={onDismiss}
          className="absolute right-3 top-2 rounded-md p-1 text-muted-foreground hover:bg-muted sm:hidden"
          aria-label={t("onboarding.bannerDismiss")}
        >
          <X className="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}

/**
 * Single top banner slot: waits for auth (and facility tablet status on the homepage)
 * before showing either the facility session bar or the onboarding prompt.
 */
export function TopSessionBanner() {
  const pathname = usePathname();
  const { user, loading: authLoading } = useAuth();
  const [dismissed, setDismissed] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);

  const isHome = pathname === "/";
  const isFacilityAuthRoute = pathname.startsWith("/facility");
  const shouldCheckFacility = !authLoading && !user && isHome && !isFacilityAuthRoute;

  const {
    facilityMode,
    hasAccount,
    loading: facilityLoading,
  } = useFacilityTabletStatus(shouldCheckFacility);

  const resolving = authLoading || (shouldCheckFacility && facilityLoading);

  useEffect(() => {
    if (resolving) return;

    setDismissed(sessionStorage.getItem(DISMISS_KEY) === "1");
    setShowOnboarding(shouldShowOnboardingPrompt(readClientPreferences()));
  }, [resolving, pathname]);

  useEffect(() => {
    const refreshOnboarding = () => {
      if (resolving) return;
      setDismissed(sessionStorage.getItem(DISMISS_KEY) === "1");
      setShowOnboarding(shouldShowOnboardingPrompt(readClientPreferences()));
    };

    window.addEventListener(PREFS_UPDATED_EVENT, refreshOnboarding);
    return () => window.removeEventListener(PREFS_UPDATED_EVENT, refreshOnboarding);
  }, [resolving]);

  const dismissOnboarding = () => {
    sessionStorage.setItem(DISMISS_KEY, "1");
    setDismissed(true);
  };

  if (resolving) return null;
  if (user || isFacilityAuthRoute) return null;

  if (shouldCheckFacility && facilityMode) {
    return <FacilitySessionBanner hasAccount={hasAccount} />;
  }

  if (!dismissed && showOnboarding) {
    return <OnboardingPromptBannerContent onDismiss={dismissOnboarding} />;
  }

  return null;
}
