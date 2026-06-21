"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";
import { pageSectionPadding } from "@/lib/utils";

export default function SignupPage() {
  const router = useRouter();
  const { signUp } = useAuth();
  const { t } = useTranslations();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    const result = await signUp(email, password, fullName);
    if (result.error) {
      setError(result.error);
      setLoading(false);
      return;
    }

    if (result.needsEmailConfirmation) {
      setSuccess(t("auth.signUpConfirmEmail"));
      setLoading(false);
      return;
    }

    router.push("/dashboard");
    router.refresh();
  };

  return (
    <div className={pageSectionPadding}>
      <div className="mx-auto max-w-md">
        <Card>
          <h1 className="mb-2 text-2xl font-bold">{t("auth.signUp")}</h1>
          <p className="mb-8 text-base text-muted-foreground">{t("auth.signUpSubtitle")}</p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label={t("auth.fullName")}
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              autoComplete="name"
            />
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
              minLength={8}
              hint={t("auth.passwordHint")}
              autoComplete="new-password"
            />
            {error && (
              <p role="alert" className="text-base text-destructive">
                {error}
              </p>
            )}
            {success && (
              <p role="status" className="text-base text-primary">
                {success}
              </p>
            )}
            <Button type="submit" size="lg" className="w-full" disabled={loading}>
              {loading ? t("auth.creatingAccount") : t("auth.signUp")}
            </Button>
          </form>

          <p className="mt-6 text-center text-base text-muted-foreground">
            {t("auth.hasAccount")}{" "}
            <Link href="/login" className="font-semibold text-primary hover:underline">
              {t("auth.signInLink")}
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
