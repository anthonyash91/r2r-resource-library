"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useFacilityTabletStatus } from "@/hooks/use-facility-tablet-status";

export function FacilitySessionBar() {
  const { user, loading } = useAuth();
  const { t } = useTranslations();
  const shouldFetch = !loading && !user;
  const { facilityMode, hasAccount, loading: statusLoading } = useFacilityTabletStatus(shouldFetch);

  if (!facilityMode || loading || user || statusLoading) return null;

  return (
    <div className="border-b border-primary/20 bg-secondary/80 px-4 py-4 sm:px-6 lg:px-8">
      <div
        className={cn(
          "mx-auto max-w-7xl",
          !hasAccount && "flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
        )}
      >
        {hasAccount ? (
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-base font-semibold text-foreground">{t("facility.barSignInTitle")}</p>
            <p className="mt-1 text-base text-foreground">{t("facility.barSignInDesc")}</p>
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
