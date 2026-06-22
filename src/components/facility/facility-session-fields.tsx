"use client";

import { Input } from "@/components/ui/input";
import { useTranslations } from "@/i18n/locale-context";

interface FacilitySessionFieldsProps {
  facilityName: string;
  pin?: string;
  showPin?: boolean;
}

export function FacilitySessionFields({
  facilityName,
  pin,
  showPin = true,
}: FacilitySessionFieldsProps) {
  const { t } = useTranslations();

  return (
    <div className="space-y-5 rounded-xl border border-border bg-muted/40 p-4">
      <Input
        label={t("facility.facilityLabel")}
        value={facilityName}
        disabled
        readOnly
        hint={t("facility.facilityRecordedHint")}
        autoComplete="off"
      />
      {showPin && pin ? (
        <Input
          label={t("facility.usernameLabel")}
          value={pin}
          disabled
          readOnly
          hint={t("facility.usernameHint")}
          autoComplete="username"
        />
      ) : null}
    </div>
  );
}
