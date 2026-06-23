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

const bannerShellClass = "border-b border-primary/20 bg-secondary/80 px-4 py-4 sm:px-6 lg:px-8";

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
      <div className="mx-auto flex max-w-7xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="pr-8 sm:pr-0">
          <p className="text-base font-semibold text-foreground">{t("onboarding.bannerTitle")}</p>
          <p className="mt-1 text-sm text-muted-foreground">{t("onboarding.bannerDesc")}</p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Link href="/get-started">
            <Button size="sm">{t("onboarding.bannerCta")}</Button>
          </Link>
          <Button type="button" variant="ghost" size="sm" onClick={onDismiss}>
            {t("onboarding.bannerDismiss")}
          </Button>
        </div>
        <button
          type="button"
          onClick={onDismiss}
          className="absolute right-3 top-3 rounded-lg p-2 text-muted-foreground hover:bg-muted sm:hidden"
          aria-label={t("onboarding.bannerDismiss")}
        >
          <X className="h-5 w-5" aria-hidden="true" />
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
