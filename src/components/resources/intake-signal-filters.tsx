"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useTransition } from "react";
import { cn } from "@/lib/utils";
import { buildResourcesPageHref } from "@/lib/resources-page";
import {
  INTAKE_SIGNALS,
  parseIntakeFilterParam,
  serializeIntakeFilterParam,
  type IntakeSignal,
} from "@/lib/intake-signals";
import { useTranslations } from "@/i18n/locale-context";

interface IntakeSignalFiltersProps {
  compact?: boolean;
}

export function IntakeSignalFilters({ compact = false }: IntakeSignalFiltersProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();
  const { t } = useTranslations();

  const active = parseIntakeFilterParam(searchParams.get("intake"));

  const toggleSignal = useCallback(
    (signal: IntakeSignal) => {
      const next = active.includes(signal)
        ? active.filter((item) => item !== signal)
        : [...active, signal];

      const params = new URLSearchParams(searchParams.toString());
      if (next.length > 0) {
        params.set("intake", serializeIntakeFilterParam(next));
      } else {
        params.delete("intake");
      }

      startTransition(() => {
        router.push(buildResourcesPageHref(params, "results"), { scroll: false });
      });
    },
    [active, router, searchParams]
  );

  return (
    <fieldset
      className={cn("min-w-0", compact ? "space-y-2" : "space-y-3")}
      disabled={isPending}
    >
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
          const selected = active.includes(signal);
          return (
            <button
              key={signal}
              type="button"
              aria-pressed={selected}
              onClick={() => toggleSignal(signal)}
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
