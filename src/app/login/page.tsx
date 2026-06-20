"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";

export default function LoginPage() {
  const router = useRouter();
  const { signIn } = useAuth();
  const { t } = useTranslations();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

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

    router.push(email.includes("admin") ? "/admin" : "/dashboard");
    router.refresh();
  };

  return (
    <div className="px-4 py-16 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-md">
        <Card>
          <h1 className="mb-2 text-2xl font-bold">{t("auth.signIn")}</h1>
          <p className="mb-8 text-base text-muted-foreground">{t("auth.signInSubtitle")}</p>

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
            {error && (
              <p role="alert" className="text-base text-destructive">
                {error}
              </p>
            )}
            <Button type="submit" size="lg" className="w-full" disabled={loading}>
              {loading ? t("auth.signingIn") : t("auth.signIn")}
            </Button>
          </form>

          <p className="mt-6 text-center text-base text-muted-foreground">
            {t("auth.noAccount")}{" "}
            <Link href="/signup" className="font-semibold text-primary hover:underline">
              {t("auth.createOneFree")}
            </Link>
          </p>

          {!process.env.NEXT_PUBLIC_SUPABASE_URL && (
            <p className="mt-4 rounded-lg bg-secondary p-3 text-sm text-muted-foreground">
              {t("auth.demoMode")}
            </p>
          )}
        </Card>
      </div>
    </div>
  );
}
