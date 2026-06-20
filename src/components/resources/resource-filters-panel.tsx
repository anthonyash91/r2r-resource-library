"use client";

import { useState } from "react";
import { ChevronDown, SlidersHorizontal } from "lucide-react";
import { cn, blockInsetPadding } from "@/lib/utils";
import { ResourceFiltersBar } from "./resource-filters";
import type { Category } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

interface ResourceFiltersPanelProps {
  categories: Category[];
  states: string[];
  counties: string[];
  cities: string[];
  services: string[];
}

export function ResourceFiltersPanel(props: ResourceFiltersPanelProps) {
  const [open, setOpen] = useState(false);
  const { t } = useTranslations();

  return (
    <div className="w-full min-w-0 rounded-xl border border-border bg-card">
      <button
        type="button"
        className={cn(
          "flex w-full min-w-0 cursor-pointer items-center justify-between gap-3 text-left",
          blockInsetPadding,
          !open && "min-h-[52px] rounded-xl",
          open && "rounded-t-xl"
        )}
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-controls="resource-filters-panel"
      >
        <span className="flex min-w-0 flex-1 items-center gap-2 text-sm font-semibold leading-snug sm:text-base">
          <SlidersHorizontal className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
          <span className="min-w-0">{t("resources.locationFilters")}</span>
        </span>
        <ChevronDown
          className={cn("h-5 w-5 shrink-0 transition-transform", open && "rotate-180")}
          aria-hidden="true"
        />
      </button>
      {open && (
        <div
          id="resource-filters-panel"
          className="rounded-b-xl border-t border-border px-4 pb-5 pt-4 sm:px-5"
        >
          <ResourceFiltersBar {...props} embedded />
        </div>
      )}
    </div>
  );
}
