"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useTranslations } from "@/i18n/locale-context";
import { pageSectionPadding } from "@/lib/utils";

type FacilityStatus = {
  pinMasked?: string;
  hasAccount?: boolean;
};

export function FacilityLoginForm() {
  const { t } = useTranslations();
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionReady, setSessionReady] = useState<boolean | null>(null);
  const [hasAccount, setHasAccount] = useState(true);
  const [facilityStatus, setFacilityStatus] = useState<FacilityStatus>({});

  useEffect(() => {
    fetch("/api/facility/status")
      .then(async (res) => {
        if (!res.ok) {
          setSessionReady(false);
          return;
        }
        const data = (await res.json()) as FacilityStatus;
        setSessionReady(true);
        setHasAccount(Boolean(data.hasAccount));
        setFacilityStatus(data);
      })
      .catch(() => setSessionReady(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const result = await fetch("/api/auth/facility-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });

    if (!result.ok) {
      const payload = (await result.json().catch(() => ({}))) as { error?: string };
      setError(payload.error ?? t("auth.signInFailed"));
      setLoading(false);
      return;
    }

    window.location.assign("/dashboard");
  };

  if (sessionReady === null) {
    return (
      <div className={pageSectionPadding}>
        <p className="text-center text-lg text-muted-foreground">{t("common.loading")}</p>
      </div>
    );
  }

  if (!sessionReady) {
    return (
      <div className={pageSectionPadding}>
        <Card className="mx-auto max-w-md">
          <h1 className="mb-2 text-2xl font-bold">{t("facility.sessionRequiredTitle")}</h1>
          <p className="text-base text-muted-foreground">{t("facility.sessionRequired")}</p>
        </Card>
      </div>
    );
  }

  if (!hasAccount) {
    return (
      <div className={pageSectionPadding}>
        <Card className="mx-auto max-w-md">
          <h1 className="mb-2 text-2xl font-bold">{t("facility.noAccountTitle")}</h1>
          <p className="mb-6 text-base text-muted-foreground">{t("facility.noAccountDesc")}</p>
          <Link href="/facility/signup">
            <Button size="lg" className="w-full">
              {t("facility.createAccount")}
            </Button>
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className={pageSectionPadding}>
      <div className="mx-auto max-w-md">
        <Card>
          <h1 className="mb-4 text-2xl font-bold">{t("facility.loginTitle")}</h1>

          <form onSubmit={handleSubmit} className="space-y-5">
            {facilityStatus.pinMasked ? (
              <div className="space-y-3">
                <Input
                  label={t("facility.usernameLabel")}
                  value={facilityStatus.pinMasked}
                  disabled
                  readOnly
                  autoComplete="username"
                />
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {t("facility.loginPinNotNeededNote")}
                </p>
              </div>
            ) : null}
            <Input
              label={t("auth.password")}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
            {error ? (
              <p role="alert" className="text-base text-destructive">
                {error}
              </p>
            ) : null}
            <Button type="submit" size="lg" className="w-full" loading={loading}>
              {loading ? t("auth.signingIn") : t("auth.signIn")}
            </Button>
          </form>

          <p className="mt-6 text-center text-base">
            <Link href="/facility/forgot-password" className="font-semibold text-primary hover:underline">
              {t("facility.forgotPassword")}
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
