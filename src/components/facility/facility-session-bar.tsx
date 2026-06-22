"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";
import { Button } from "@/components/ui/button";

export function FacilitySessionBar() {
  const { user, loading } = useAuth();
  const { t } = useTranslations();
  const [facilityMode, setFacilityMode] = useState(false);
  const [hasAccount, setHasAccount] = useState(false);

  useEffect(() => {
    fetch("/api/facility/status")
      .then(async (res) => {
        if (!res.ok) {
          setFacilityMode(false);
          return;
        }
        const data = (await res.json()) as { hasAccount?: boolean };
        setFacilityMode(true);
        setHasAccount(Boolean(data.hasAccount));
      })
      .catch(() => setFacilityMode(false));
  }, []);

  if (!facilityMode || loading || user) return null;

  return (
    <div className="border-b border-primary/20 bg-secondary/80 px-4 py-4 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-base font-semibold text-foreground">{t("facility.barTitle")}</p>
          <p className="mt-1 text-sm text-muted-foreground">{t("facility.barDesc")}</p>
          <p className="mt-1 text-sm text-muted-foreground">{t("facility.privacyReminder")}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {hasAccount ? (
            <Link href="/facility/login">
              <Button size="sm">{t("facility.goToLogin")}</Button>
            </Link>
          ) : (
            <Link href="/facility/signup">
              <Button size="sm">{t("facility.createAccount")}</Button>
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
