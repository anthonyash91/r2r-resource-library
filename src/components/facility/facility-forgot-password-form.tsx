"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useTranslations } from "@/i18n/locale-context";
import { pageSectionPadding } from "@/lib/utils";

export function FacilityForgotPasswordForm() {
  const router = useRouter();
  const { t } = useTranslations();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [answer1, setAnswer1] = useState("");
  const [answer2, setAnswer2] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [sessionReady, setSessionReady] = useState<boolean | null>(null);

  useEffect(() => {
    fetch("/api/facility/status")
      .then((res) => setSessionReady(res.ok))
      .catch(() => setSessionReady(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    const res = await fetch("/api/auth/facility-reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, answer1, answer2 }),
    });

    if (!res.ok) {
      const payload = (await res.json().catch(() => ({}))) as { error?: string };
      setError(payload.error ?? t("facility.resetFailed"));
      setLoading(false);
      return;
    }

    setSuccess(true);
    setLoading(false);
    setTimeout(() => {
      router.push("/facility/login");
    }, 2000);
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

  return (
    <div className={pageSectionPadding}>
      <div className="mx-auto max-w-md">
        <Card>
          <h1 className="mb-2 text-2xl font-bold">{t("facility.resetTitle")}</h1>
          <p className="mb-8 text-base text-muted-foreground">{t("facility.resetSubtitle")}</p>

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
              label={t("facility.newPasswordLabel")}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              autoComplete="new-password"
            />
            <Input
              label={t("facility.resetAnswer1Label")}
              value={answer1}
              onChange={(e) => setAnswer1(e.target.value)}
              required
              autoComplete="off"
            />
            <Input
              label={t("facility.resetAnswer2Label")}
              value={answer2}
              onChange={(e) => setAnswer2(e.target.value)}
              required
              autoComplete="off"
            />
            {error ? (
              <p role="alert" className="text-base text-destructive">
                {error}
              </p>
            ) : null}
            {success ? (
              <p role="status" className="text-base text-primary">
                {t("facility.resetSuccess")}
              </p>
            ) : null}
            <Button type="submit" size="lg" className="w-full" disabled={loading || success}>
              {loading ? t("facility.resetting") : t("facility.resetPassword")}
            </Button>
          </form>

          <p className="mt-6 text-center text-base">
            <Link href="/facility/login" className="font-semibold text-primary hover:underline">
              {t("facility.backToLogin")}
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
