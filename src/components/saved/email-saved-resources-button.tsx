"use client";

import { useState } from "react";
import { CheckCircle2, Info, Mail } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Modal } from "@/components/ui/modal";
import { useAuth } from "@/lib/auth-context";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";
import { cn, checkIconClass } from "@/lib/utils";
import { isFacilityAuthEmail } from "@/lib/facility/auth-email";
import type { SavedPdfEmailStatus } from "@/lib/saved-pdf-email";
import type { Profile } from "@/types";

interface EmailSavedResourcesButtonProps {
  resourceCount: number;
  variant?: "primary" | "outline";
  size?: "sm" | "md" | "lg";
}

function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

function defaultPdfEmail(user: Profile): string {
  if (user.contact_email?.trim()) return user.contact_email.trim();
  if (user.signup_context === "facility" && isFacilityAuthEmail(user.email)) return "";
  return user.email ?? "";
}

export function EmailSavedResourcesButton({
  resourceCount,
  variant = "outline",
  size = "md",
}: EmailSavedResourcesButtonProps) {
  const { user, isAdmin } = useAuth();
  const { t } = useTranslations();
  const [open, setOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [sending, setSending] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [emailStatus, setEmailStatus] = useState<SavedPdfEmailStatus | null>(null);
  const [successEmail, setSuccessEmail] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!user || resourceCount === 0) return null;

  const limitReached = !isAdmin && emailStatus?.remaining === 0;
  const showLimitInfo = !isAdmin && emailStatus && !emailStatus.unlimited;
  const showSuccess = successEmail !== null;

  const handleOpen = async () => {
    setErrorMessage(null);
    setEmailError(null);
    setSuccessEmail(null);
    setEmail(defaultPdfEmail(user));
    setOpen(true);
    setEmailStatus(null);

    if (!isSupabaseConfigured()) {
      return;
    }

    setLoadingStatus(true);
    try {
      const response = await fetch("/api/saved-resources/email-pdf");
      const data = (await response.json()) as SavedPdfEmailStatus & { error?: string };
      if (response.ok) {
        setEmailStatus({
          sent: data.sent,
          limit: data.limit,
          remaining: data.remaining,
          unlimited: data.unlimited,
        });
      } else {
        setErrorMessage(data.error ?? t("saved.email.failed"));
      }
    } catch {
      setErrorMessage(t("saved.email.failed"));
    } finally {
      setLoadingStatus(false);
    }
  };

  const handleClose = () => {
    if (sending) return;
    setOpen(false);
    setEmailError(null);
    setEmailStatus(null);
    setSuccessEmail(null);
    setErrorMessage(null);
  };

  const handleSend = async () => {
    setErrorMessage(null);
    setEmailError(null);

    if (limitReached) {
      setErrorMessage(t("saved.email.limitReached", { limit: emailStatus?.limit ?? 3 }));
      return;
    }

    if (!isValidEmail(email)) {
      setEmailError(t("saved.email.invalidEmail"));
      return;
    }

    if (!isSupabaseConfigured()) {
      setErrorMessage(t("saved.email.unavailable"));
      return;
    }

    setSending(true);

    try {
      const response = await fetch("/api/saved-resources/email-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });
      const data = (await response.json()) as SavedPdfEmailStatus & {
        success?: boolean;
        email?: string;
        error?: string;
      };

      if (!response.ok) {
        if (typeof data.sent === "number") {
          setEmailStatus({
            sent: data.sent,
            limit: data.limit,
            remaining: data.remaining,
            unlimited: data.unlimited,
          });
        }
        setErrorMessage(data.error ?? t("saved.email.failed"));
        return;
      }

      setEmailStatus({
        sent: data.sent,
        limit: data.limit,
        remaining: data.remaining,
        unlimited: data.unlimited,
      });
      setSuccessEmail(data.email ?? email.trim());
    } catch {
      setErrorMessage(t("saved.email.failed"));
    } finally {
      setSending(false);
    }
  };

  return (
    <>
      <div className="flex flex-col items-start gap-2">
        <Button type="button" variant={variant} size={size} onClick={handleOpen}>
          <Mail className="h-5 w-5" aria-hidden="true" />
          {t("saved.email.button")}
        </Button>
        {errorMessage && !open ? (
          <p role="alert" className="text-sm text-destructive">
            {errorMessage}
          </p>
        ) : null}
      </div>

      <Modal
        open={open}
        onClose={handleClose}
        title={showSuccess ? t("saved.email.successTitle") : t("saved.email.prompt")}
        closeLabel={t("common.close")}
        disableClose={sending}
      >
        {showSuccess ? (
          <div className="space-y-4">
            <div className="flex items-start gap-3 rounded-lg border border-success/20 bg-success/5 p-4">
              <CheckCircle2
                className={cn("mt-0.5 h-5 w-5 shrink-0", checkIconClass)}
                aria-hidden="true"
              />
              <p className="text-base text-foreground" role="status">
                {t("saved.email.success", { email: successEmail })}
              </p>
            </div>
            <Button type="button" size={size} onClick={handleClose}>
              {t("common.close")}
            </Button>
          </div>
        ) : (
          <>
            <div
              className="mb-4 rounded-lg border border-primary/20 bg-primary/5 p-3 text-sm text-foreground"
              role="note"
            >
              <div className="mb-2 flex items-start gap-2">
                <Info className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                <p>{t("saved.email.usageGuidance")}</p>
              </div>
              {loadingStatus ? (
                <p className="text-muted-foreground">{t("common.loading")}</p>
              ) : showLimitInfo ? (
                <p className="font-medium">
                  {limitReached
                    ? t("saved.email.limitReached", { limit: emailStatus.limit ?? 3 })
                    : t("saved.email.limitReminder", {
                        limit: emailStatus.limit ?? 3,
                        remaining: emailStatus.remaining ?? 0,
                      })}
                </p>
              ) : null}
            </div>

            <Input
              label={t("saved.email.addressLabel")}
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setEmailError(null);
              }}
              placeholder={t("saved.email.addressPlaceholder")}
              hint={t("saved.email.addressHint")}
              error={emailError ?? undefined}
              autoComplete="email"
              disabled={sending || loadingStatus || limitReached}
            />
            <div className="mt-4 flex flex-wrap gap-2">
              <Button
                type="button"
                size={size}
                onClick={handleSend}
                loading={sending}
                disabled={loadingStatus || limitReached}
              >
                <Mail className="h-5 w-5" aria-hidden="true" />
                {sending ? t("saved.email.buttonSending") : t("saved.email.sendButton")}
              </Button>
              <Button
                type="button"
                variant="outline"
                size={size}
                onClick={handleClose}
                disabled={sending}
              >
                {t("common.cancel")}
              </Button>
            </div>
            {errorMessage ? (
              <p role="alert" className="mt-3 text-sm text-destructive">
                {errorMessage}
              </p>
            ) : null}
          </>
        )}
      </Modal>
    </>
  );
}
