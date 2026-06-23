"use client";

import { cn } from "@/lib/utils";
import { INTAKE_SIGNALS } from "@/lib/intake-signals";
import { useTranslations } from "@/i18n/locale-context";
import { useResourceFilterDraft } from "./resource-filter-draft-context";

interface IntakeSignalFiltersProps {
  compact?: boolean;
}

export function IntakeSignalFilters({ compact = false }: IntakeSignalFiltersProps) {
  const { t } = useTranslations();
  const { draft, toggleIntake } = useResourceFilterDraft();

  return (
    <fieldset className={cn("min-w-0", compact ? "space-y-2" : "space-y-3")}>
      <legend
        className={cn(
          "font-semibold text-foreground",
          compact ? "mb-2 text-sm" : "mb-3 text-base"
        )}
      >
        {t("resources.intakeFiltersLabel")}
      </legend>
      <div className="flex flex-wrap gap-2">
        {INTAKE_SIGNALS.map((signal) => {
          const selected = draft.intake.includes(signal);
          return (
            <button
              key={signal}
              type="button"
              aria-pressed={selected}
              onClick={() => toggleIntake(signal)}
              className={cn(
                "rounded-xl border px-3 py-1.5 text-sm font-medium transition-colors",
                "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
                selected
                  ? "border-primary bg-primary text-primary-foreground"
                  : "border-border bg-card text-foreground hover:border-primary/40"
              )}
            >
              {t(`resources.intakeSignals.${signal}`)}
            </button>
          );
        })}
      </div>
      <p className="text-sm text-muted-foreground">{t("resources.intakeFiltersHint")}</p>
    </fieldset>
  );
}
