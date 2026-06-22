"use client";

import { useState } from "react";
import { Mail } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";

function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

export function FacilityContactEmailSection() {
  const { user } = useAuth();
  const { t } = useTranslations();
  const [contactEmail, setContactEmail] = useState(user?.contact_email ?? "");
  const [savedEmail, setSavedEmail] = useState(user?.contact_email ?? "");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  if (!user || user.signup_context !== "facility") {
    return null;
  }

  const hasSavedContactEmail = Boolean(savedEmail?.trim());

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (!isValidEmail(contactEmail)) {
      setError(t("facility.contactEmailInvalid"));
      return;
    }

    setLoading(true);
    const res = await fetch("/api/auth/facility-contact-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contactEmail: contactEmail.trim() }),
    });

    if (!res.ok) {
      const payload = (await res.json().catch(() => ({}))) as { error?: string };
      setError(payload.error ?? t("facility.contactEmailSaveFailed"));
      setLoading(false);
      return;
    }

    const payload = (await res.json()) as { contactEmail?: string };
    const nextEmail = payload.contactEmail ?? contactEmail.trim();
    setSavedEmail(nextEmail);
    setContactEmail(nextEmail);
    setSuccess(true);
    setLoading(false);
  };

  return (
    <Card className="mb-10 p-4 sm:p-6">
      <div className="flex items-start gap-3">
        <Mail className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
        <div className="w-full">
          <h2 className="text-xl font-bold">{t("facility.contactEmailSectionTitle")}</h2>
          <p className="mt-1 text-base text-muted-foreground">
            {t("facility.contactEmailSectionDesc")}
          </p>

          {hasSavedContactEmail ? (
            <p className="mt-4 text-base font-medium">
              {t("facility.contactEmailSaved", { email: savedEmail })}
            </p>
          ) : null}

          <form onSubmit={handleSubmit} className="mt-4 space-y-4">
            <Input
              label={hasSavedContactEmail ? t("facility.contactEmailLabel") : undefined}
              type="email"
              value={contactEmail}
              onChange={(e) => {
                setContactEmail(e.target.value);
                setSuccess(false);
              }}
              placeholder={t("facility.contactEmailPlaceholder")}
              autoComplete="email"
            />
            {error ? (
              <p role="alert" className="text-base text-destructive">
                {error}
              </p>
            ) : null}
            {success ? (
              <p role="status" className="text-base text-primary">
                {t("facility.contactEmailSaved", { email: savedEmail })}
              </p>
            ) : null}
            <Button type="submit" size="sm" loading={loading}>
              {loading ? t("facility.contactEmailSaving") : t("facility.contactEmailSave")}
            </Button>
          </form>
        </div>
      </div>
    </Card>
  );
}
