"use client";

import { useState } from "react";
import { ChevronDown, SlidersHorizontal } from "lucide-react";
import { cn } from "@/lib/utils";
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
    <div className="rounded-2xl border border-border bg-card">
      <button
        type="button"
        className="flex w-full min-h-[48px] cursor-pointer items-center justify-between gap-3 px-5 py-3 text-left"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-controls="resource-filters-panel"
      >
        <span className="flex items-center gap-2 text-base font-semibold">
          <SlidersHorizontal className="h-5 w-5 text-primary" aria-hidden="true" />
          {t("resources.locationFilters")}
        </span>
        <ChevronDown
          className={cn("h-5 w-5 shrink-0 transition-transform", open && "rotate-180")}
          aria-hidden="true"
        />
      </button>
      {open && (
        <div id="resource-filters-panel" className="border-t border-border p-5">
          <ResourceFiltersBar {...props} hideCategory embedded />
        </div>
      )}
    </div>
  );
}
