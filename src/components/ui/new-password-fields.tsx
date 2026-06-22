"use client";

import { PasswordInput } from "@/components/ui/password-input";
import { PasswordStrengthMeter } from "@/components/ui/password-strength-meter";
import { useTranslations } from "@/i18n/locale-context";

interface NewPasswordFieldsProps {
  password: string;
  confirmPassword: string;
  onPasswordChange: (value: string) => void;
  onConfirmPasswordChange: (value: string) => void;
  passwordLabel: string;
  confirmLabel: string;
  passwordId?: string;
  confirmId?: string;
  minLength?: number;
  showHint?: boolean;
  passwordAutoComplete?: string;
  confirmAutoComplete?: string;
}

export function NewPasswordFields({
  password,
  confirmPassword,
  onPasswordChange,
  onConfirmPasswordChange,
  passwordLabel,
  confirmLabel,
  passwordId = "new-password",
  confirmId = "confirm-password",
  minLength = 8,
  showHint = true,
  passwordAutoComplete = "new-password",
  confirmAutoComplete = "new-password",
}: NewPasswordFieldsProps) {
  const { t } = useTranslations();
  const mismatch = confirmPassword.length > 0 && password !== confirmPassword;

  return (
    <div className="space-y-5">
      <div className="space-y-2">
        <PasswordInput
          id={passwordId}
          label={passwordLabel}
          value={password}
          onChange={(e) => onPasswordChange(e.target.value)}
          required
          minLength={minLength}
          hint={showHint ? t("auth.passwordHint") : undefined}
          autoComplete={passwordAutoComplete}
        />
        <PasswordStrengthMeter password={password} />
      </div>
      <PasswordInput
        id={confirmId}
        label={confirmLabel}
        value={confirmPassword}
        onChange={(e) => onConfirmPasswordChange(e.target.value)}
        required
        minLength={minLength}
        autoComplete={confirmAutoComplete}
        error={mismatch ? t("auth.passwordMismatch") : undefined}
      />
    </div>
  );
}

export function passwordsMatch(password: string, confirmPassword: string): boolean {
  return password.length > 0 && password === confirmPassword;
}
