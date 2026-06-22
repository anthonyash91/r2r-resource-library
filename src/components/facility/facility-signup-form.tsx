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

export function FacilitySignupForm() {
  const router = useRouter();
  const { signIn } = useAuth();
  const { t } = useTranslations();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [recoveryQuestion1, setRecoveryQuestion1] = useState("");
  const [recoveryAnswer1, setRecoveryAnswer1] = useState("");
  const [recoveryQuestion2, setRecoveryQuestion2] = useState("");
  const [recoveryAnswer2, setRecoveryAnswer2] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionReady, setSessionReady] = useState<boolean | null>(null);
  const [hasAccount, setHasAccount] = useState(false);

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

    const signupRes = await fetch("/api/auth/facility-signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        fullName,
        recoveryQuestion1,
        recoveryAnswer1,
        recoveryQuestion2,
        recoveryAnswer2,
      }),
    });

    if (!signupRes.ok) {
      const payload = (await signupRes.json().catch(() => ({}))) as { error?: string };
      setError(payload.error ?? t("auth.signUpFailed"));
      setLoading(false);
      return;
    }

    const signInResult = await signIn(email, password);
    if (signInResult.error) {
      setError(signInResult.error);
      setLoading(false);
      return;
    }

    router.replace("/get-started");
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

  if (hasAccount) {
    return (
      <div className={pageSectionPadding}>
        <Card className="mx-auto max-w-md">
          <h1 className="mb-2 text-2xl font-bold">{t("facility.accountAlreadyExistsTitle")}</h1>
          <p className="mb-6 text-base text-muted-foreground">
            {t("facility.accountAlreadyExistsDesc")}
          </p>
          <Link href="/facility/login">
            <Button size="lg" className="w-full">
              {t("facility.goToLogin")}
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
          <h1 className="mb-2 text-2xl font-bold">{t("facility.signupTitle")}</h1>
          <p className="mb-8 text-base text-muted-foreground">{t("facility.signupSubtitle")}</p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label={t("auth.fullName")}
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              autoComplete="name"
            />
            <Input
              label={t("facility.accountEmailLabel")}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              hint={t("facility.accountEmailHint")}
            />
            <Input
              label={t("auth.password")}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              hint={t("auth.passwordHint")}
              autoComplete="new-password"
            />
            <Input
              label={t("facility.recoveryQuestion1Label")}
              value={recoveryQuestion1}
              onChange={(e) => setRecoveryQuestion1(e.target.value)}
              required
              hint={t("facility.recoveryQuestionHint")}
            />
            <Input
              label={t("facility.recoveryAnswer1Label")}
              value={recoveryAnswer1}
              onChange={(e) => setRecoveryAnswer1(e.target.value)}
              required
              autoComplete="off"
            />
            <Input
              label={t("facility.recoveryQuestion2Label")}
              value={recoveryQuestion2}
              onChange={(e) => setRecoveryQuestion2(e.target.value)}
              required
              hint={t("facility.recoveryQuestionHint")}
            />
            <Input
              label={t("facility.recoveryAnswer2Label")}
              value={recoveryAnswer2}
              onChange={(e) => setRecoveryAnswer2(e.target.value)}
              required
              autoComplete="off"
            />
            {error ? (
              <p role="alert" className="text-base text-destructive">
                {error}
              </p>
            ) : null}
            <Button type="submit" size="lg" className="w-full" disabled={loading}>
              {loading ? t("auth.creatingAccount") : t("facility.createAccount")}
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
}
