"use client";

import { useMemo, useTransition } from "react";
import { Search, X } from "lucide-react";
import { Dropdown } from "@/components/ui/dropdown";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { Category } from "@/types";
import { useTranslations } from "@/i18n/locale-context";
import { useCategoryLabel } from "@/i18n/use-category-label";
import { getCountiesForState } from "@/lib/states/registry";
import { useResourceFilterDraft } from "./resource-filter-draft-context";
import { IntakeSignalFilters } from "./intake-signal-filters";

interface ResourceFiltersProps {
  categories: Category[];
  states: string[];
  counties: string[];
  cities: string[];
  services: string[];
  embedded?: boolean;
  compact?: boolean;
}

export function ResourceFiltersBar({
  categories,
  states,
  counties,
  cities,
  services,
  embedded = false,
  compact = false,
}: ResourceFiltersProps) {
  const [isPending, startTransition] = useTransition();
  const { t } = useTranslations();
  const categoryLabel = useCategoryLabel();
  const { draft, applied, setField, apply, clear, hasDraftFilters, hasAppliedFilters } =
    useResourceFilterDraft();

  const countyOptions = useMemo(() => {
    if (draft.state) {
      const canonical = getCountiesForState(draft.state);
      if (canonical.length > 0) return canonical;
    }
    return counties;
  }, [counties, draft.state]);

  const cityOptions = useMemo(() => {
    if (draft.state === applied.state && draft.county === applied.county) {
      return cities;
    }
    return [];
  }, [applied.county, applied.state, cities, draft.county, draft.state]);

  const handleApply = () => {
    startTransition(() => {
      apply();
    });
  };

  const handleClear = () => {
    startTransition(() => {
      clear();
    });
  };

  const withPlaceholder = (items: string[], placeholder: string) => [
    { value: "", label: placeholder },
    ...items.map((item) => ({ value: item, label: item })),
  ];

  return (
    <div
      className={cn(
        "w-full min-w-0 max-w-full",
        embedded ? "space-y-4" : "space-y-4 rounded-xl border border-border bg-card p-4 sm:p-6"
      )}
      role="group"
      aria-label={t("resources.filterAria")}
    >
      <div
        className={cn(
          "grid min-w-0 grid-cols-1 gap-4",
          compact ? "sm:grid-cols-2 lg:grid-cols-3" : "md:grid-cols-2 xl:grid-cols-3"
        )}
      >
        <Dropdown
          label={t("resources.category")}
          placeholder={t("resources.allCategories")}
          value={draft.category}
          onChange={(value) => setField("category", value)}
          options={[
            { value: "", label: t("resources.allCategories") },
            ...categories.map((c) => ({ value: c.slug, label: categoryLabel(c) })),
          ]}
          searchPlaceholder={t("resources.searchCategories")}
        />
        <Dropdown
          label={t("resources.state")}
          placeholder={t("resources.allStates")}
          value={draft.state}
          onChange={(value) => setField("state", value)}
          options={withPlaceholder(states, t("resources.allStates"))}
          searchPlaceholder={t("resources.searchStates")}
        />
        <Dropdown
          label={t("resources.county")}
          placeholder={t("resources.allCounties")}
          value={draft.county}
          onChange={(value) => setField("county", value)}
          options={withPlaceholder(countyOptions, t("resources.allCounties"))}
          searchPlaceholder={t("resources.searchCounties")}
          disabled={!draft.state}
        />
        <p
          className={cn(
            "text-sm text-muted-foreground",
            compact ? "sm:col-span-2 lg:col-span-3" : "md:col-span-2 xl:col-span-3"
          )}
        >
          {t("resources.countyFilterHint")}
        </p>
        <Dropdown
          label={t("resources.city")}
          placeholder={t("resources.allCities")}
          value={draft.city}
          onChange={(value) => setField("city", value)}
          options={withPlaceholder(cityOptions, t("resources.allCities"))}
          searchPlaceholder={t("resources.searchCities")}
          disabled={!draft.county || cityOptions.length === 0}
        />
        <Dropdown
          label={t("resources.serviceType")}
          placeholder={t("resources.allServices")}
          value={draft.service}
          onChange={(value) => setField("service", value)}
          options={withPlaceholder(services, t("resources.allServices"))}
          searchPlaceholder={t("resources.searchServices")}
        />
        <Dropdown
          label={t("resources.sortFilter")}
          placeholder={t("common.default")}
          value={draft.filter}
          onChange={(value) => setField("filter", value)}
          searchable={false}
          options={[
            { value: "", label: t("common.default") },
            { value: "recent", label: t("resources.recentlyAdded") },
          ]}
        />
      </div>

      <IntakeSignalFilters compact={compact} />

      <p className="text-sm text-muted-foreground">{t("resources.filtersApplyHint")}</p>

      <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap">
        <Button
          type="button"
          className="w-full sm:w-auto"
          onClick={handleApply}
          loading={isPending}
        >
          <Search className="h-5 w-5" aria-hidden="true" />
          {t("resources.searchButton")}
        </Button>
        {hasDraftFilters || hasAppliedFilters ? (
          <Button
            type="button"
            variant="outline"
            className="w-full sm:w-auto"
            onClick={handleClear}
            disabled={isPending}
          >
            <X className="h-5 w-5" aria-hidden="true" />
            {t("resources.clearFilters")}
          </Button>
        ) : null}
      </div>
    </div>
  );
}
