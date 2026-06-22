"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { NewPasswordFields, passwordsMatch } from "@/components/ui/new-password-fields";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useTranslations } from "@/i18n/locale-context";
import { pageSectionPadding } from "@/lib/utils";

type ResetStep = "pin" | "questions" | "password";

export function FacilityForgotPasswordForm() {
  const router = useRouter();
  const { t } = useTranslations();
  const [step, setStep] = useState<ResetStep>("pin");
  const [pin, setPin] = useState("");
  const [recoveryQuestion1, setRecoveryQuestion1] = useState("");
  const [recoveryQuestion2, setRecoveryQuestion2] = useState("");
  const [answer1, setAnswer1] = useState("");
  const [answer2, setAnswer2] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [sessionReady, setSessionReady] = useState<boolean | null>(null);

  useEffect(() => {
    fetch("/api/facility/status")
      .then(async (res) => {
        setSessionReady(res.ok);
      })
      .catch(() => setSessionReady(false));
  }, []);

  const handleVerifyPin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const res = await fetch("/api/auth/facility-reset-password/verify-pin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pin }),
    });

    if (!res.ok) {
      const payload = (await res.json().catch(() => ({}))) as { error?: string };
      setError(payload.error ?? t("facility.resetPinInvalid"));
      setLoading(false);
      return;
    }

    const data = (await res.json()) as {
      recoveryQuestion1: string;
      recoveryQuestion2: string;
    };

    setRecoveryQuestion1(data.recoveryQuestion1);
    setRecoveryQuestion2(data.recoveryQuestion2);
    setAnswer1("");
    setAnswer2("");
    setStep("questions");
    setLoading(false);
  };

  const handleVerifyAnswers = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const res = await fetch("/api/auth/facility-reset-password/verify-answers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pin, answer1, answer2 }),
    });

    if (!res.ok) {
      const payload = (await res.json().catch(() => ({}))) as { error?: string };
      setError(payload.error ?? t("facility.resetAnswersWrong"));
      setLoading(false);
      return;
    }

    setPassword("");
    setConfirmPassword("");
    setStep("password");
    setLoading(false);
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (!passwordsMatch(password, confirmPassword)) {
      setError(t("auth.passwordMismatch"));
      return;
    }

    setLoading(true);

    const res = await fetch("/api/auth/facility-reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
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
          <div className="mb-4">
            <h1 className="text-2xl font-bold">{t("facility.resetTitle")}</h1>
            <p className="mt-2 text-base text-muted-foreground">
              {step === "pin"
                ? t("facility.resetPinStepDesc")
                : step === "questions"
                  ? t("facility.resetQuestionsStepDesc")
                  : t("facility.resetPasswordStepDesc")}
            </p>
          </div>

          {step === "pin" ? (
            <form onSubmit={handleVerifyPin} className="space-y-5">
              <Input
                label={t("facility.usernameLabel")}
                value={pin}
                onChange={(e) => setPin(e.target.value)}
                required
                inputMode="numeric"
                autoComplete="username"
                hint={t("facility.resetPinStepHint")}
              />
              {error ? (
                <p role="alert" className="text-base text-destructive">
                  {error}
                </p>
              ) : null}
              <Button type="submit" size="lg" className="w-full" loading={loading}>
                {t("facility.resetContinue")}
              </Button>
            </form>
          ) : null}

          {step === "questions" ? (
            <form onSubmit={handleVerifyAnswers} className="space-y-5">
              <Input
                label={recoveryQuestion1}
                value={answer1}
                onChange={(e) => setAnswer1(e.target.value)}
                required
                autoComplete="off"
              />
              <Input
                label={recoveryQuestion2}
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
              <div className="flex flex-col gap-3 sm:flex-row">
                <Button
                  type="button"
                  variant="outline"
                  size="lg"
                  className="w-full"
                  onClick={() => {
                    setError("");
                    setStep("pin");
                  }}
                >
                  {t("onboarding.back")}
                </Button>
                <Button type="submit" size="lg" className="w-full" loading={loading}>
                  {t("facility.resetContinue")}
                </Button>
              </div>
            </form>
          ) : null}

          {step === "password" ? (
            <form onSubmit={handleResetPassword} className="space-y-5">
              <NewPasswordFields
                password={password}
                confirmPassword={confirmPassword}
                onPasswordChange={setPassword}
                onConfirmPasswordChange={setConfirmPassword}
                passwordLabel={t("facility.newPasswordLabel")}
                confirmLabel={t("auth.confirmPassword")}
                passwordId="reset-password"
                confirmId="reset-confirm-password"
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
              <Button type="submit" size="lg" className="w-full" loading={loading} disabled={success}>
                {loading ? t("facility.resetting") : t("facility.resetPassword")}
              </Button>
            </form>
          ) : null}

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
