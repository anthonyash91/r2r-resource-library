"use client";

import { useState } from "react";
import { ChevronDown, SlidersHorizontal } from "lucide-react";
import { cn } from "@/lib/utils";
import { ResourceFiltersBar } from "./resource-filters";
import type { ResourceFilterOptions } from "./use-resource-filter-options";
import { useTranslations } from "@/i18n/locale-context";

interface ResourceFiltersPanelProps {
  states: string[];
  globalOptions: ResourceFilterOptions;
  appliedOptions: ResourceFilterOptions;
}

export function ResourceFiltersPanel({ ...props }: ResourceFiltersPanelProps) {
  const [open, setOpen] = useState(false);
  const { t } = useTranslations();

  return (
    <div className="w-full min-w-0 text-left">
      <button
        type="button"
        className={cn(
          "flex w-full min-w-0 cursor-pointer items-center justify-between gap-3 rounded-xl border border-primary-foreground/25 bg-primary-foreground/10 px-4 py-3 text-left backdrop-blur-sm transition-colors",
          "hover:bg-primary-foreground/15 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        )}
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-controls="resource-filters-hero-panel"
      >
        <span className="flex min-w-0 flex-1 items-center gap-2 text-base font-semibold leading-snug text-primary-foreground">
          <SlidersHorizontal className="h-5 w-5 shrink-0" aria-hidden="true" />
          <span className="min-w-0">{t("resources.locationFilters")}</span>
        </span>
        <ChevronDown
          className={cn(
            "h-5 w-5 shrink-0 text-primary-foreground/80 transition-transform",
            open && "rotate-180"
          )}
          aria-hidden="true"
        />
      </button>
      {open ? (
        <div
          id="resource-filters-hero-panel"
          className="mt-3 rounded-2xl bg-card p-4 shadow-lg sm:p-5"
        >
          <ResourceFiltersBar {...props} embedded compact />
        </div>
      ) : null}
    </div>
  );
}
