"use client";

import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";
import { scorePassword } from "@/lib/password-strength";

interface PasswordStrengthMeterProps {
  password: string;
}

const STRENGTH_KEYS = [
  "auth.passwordStrengthWeak",
  "auth.passwordStrengthFair",
  "auth.passwordStrengthGood",
  "auth.passwordStrengthStrong",
] as const;

const STRENGTH_COLORS = [
  "bg-destructive",
  "bg-orange-500",
  "bg-amber-500",
  "bg-primary",
] as const;

export function PasswordStrengthMeter({ password }: PasswordStrengthMeterProps) {
  const { t } = useTranslations();
  const score = scorePassword(password);

  if (!password) return null;

  const labelKey = STRENGTH_KEYS[Math.max(0, score - 1)];
  const activeColor = STRENGTH_COLORS[Math.max(0, score - 1)];

  return (
    <div
      role="meter"
      aria-valuemin={0}
      aria-valuemax={4}
      aria-valuenow={score}
      aria-label={t("auth.passwordStrengthLabel")}
      className="space-y-2"
    >
      <div className="flex gap-1.5">
        {[1, 2, 3, 4].map((level) => (
          <div
            key={level}
            className={cn(
              "h-1.5 flex-1 rounded-full transition-colors",
              level <= score ? activeColor : "bg-muted"
            )}
          />
        ))}
      </div>
      <p className="text-sm text-muted-foreground">{t(labelKey)}</p>
    </div>
  );
}
