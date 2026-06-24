"use client";

import { useEffect } from "react";
import { cn } from "@/lib/utils";
import { INTAKE_SIGNALS } from "@/lib/intake-signals";
import { useTranslations } from "@/i18n/locale-context";
import { useResourceFilterDraft } from "./resource-filter-draft-context";
import type { ResourceFilterOptions } from "./use-resource-filter-options";

interface IntakeSignalFiltersProps {
  intakeCounts: ResourceFilterOptions["intakeCounts"];
  isLoading?: boolean;
}

export function IntakeSignalFilters({
  intakeCounts,
  isLoading = false,
}: IntakeSignalFiltersProps) {
  const { t } = useTranslations();
  const { draft, toggleIntake, setIntake } = useResourceFilterDraft();

  useEffect(() => {
    if (isLoading) return;
    const available = draft.intake.filter((signal) => (intakeCounts[signal] ?? 0) > 0);
    if (available.length !== draft.intake.length) {
      setIntake(available);
    }
  }, [draft.intake, intakeCounts, isLoading, setIntake]);

  return (
    <fieldset className="min-w-0 space-y-3" aria-busy={isLoading}>
      <legend className="mb-2 block text-base font-semibold text-foreground">
        {t("resources.intakeFiltersLabel")}
      </legend>
      <div className="flex flex-wrap gap-2">
        {INTAKE_SIGNALS.map((signal) => {
          const selected = draft.intake.includes(signal);
          const count = intakeCounts[signal] ?? 0;
          const unavailable = !isLoading && count === 0;
          const disabled = isLoading || unavailable;
          const label = t(`resources.intakeSignals.${signal}`);

          return (
            <button
              key={signal}
              type="button"
              aria-pressed={selected}
              disabled={disabled}
              aria-label={
                unavailable
                  ? t("resources.intakeSignalUnavailableAria", { label })
                  : label
              }
              onClick={() => toggleIntake(signal)}
              className={cn(
                "rounded-xl border px-3 py-1.5 text-sm font-medium transition-colors",
                "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
                unavailable &&
                  "cursor-not-allowed border-border/60 bg-muted/40 text-muted-foreground opacity-60",
                isLoading &&
                  !unavailable &&
                  "cursor-wait border-border bg-card text-foreground opacity-80",
                !disabled &&
                  selected &&
                  "border-primary bg-primary text-primary-foreground",
                !disabled &&
                  !selected &&
                  "border-border bg-card text-foreground hover:border-primary/40"
              )}
            >
              {label}
            </button>
          );
        })}
      </div>
      <p className="text-sm text-muted-foreground">{t("resources.intakeFiltersHint")}</p>
    </fieldset>
  );
}
