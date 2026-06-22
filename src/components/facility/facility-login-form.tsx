"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";
import { pageSectionPadding } from "@/lib/utils";

export function FacilityLoginForm() {
  const router = useRouter();
  const { signIn } = useAuth();
  const { t } = useTranslations();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionReady, setSessionReady] = useState<boolean | null>(null);
  const [hasAccount, setHasAccount] = useState(true);

  useEffect(() => {
    fetch("/api/facility/status")
      .then(async (res) => {
        if (!res.ok) {
          setSessionReady(false);
          return;
        }
        const data = (await res.json()) as { hasAccount?: boolean };
        setSessionReady(true);
        setHasAccount(Boolean(data.hasAccount));
      })
      .catch(() => setSessionReady(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const result = await signIn(email, password);
    if (result.error) {
      setError(result.error);
      setLoading(false);
      return;
    }

    router.replace("/dashboard");
    router.refresh();
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
          <h1 className="mb-2 text-2xl font-bold">{t("facility.loginTitle")}</h1>
          <p className="mb-8 text-base text-muted-foreground">{t("facility.loginSubtitle")}</p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label={t("auth.email")}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
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
            <Button type="submit" size="lg" className="w-full" disabled={loading}>
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
