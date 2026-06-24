"use client";

import { useEffect, useTransition } from "react";
import { Search, X, Loader2 } from "lucide-react";
import { Dropdown } from "@/components/ui/dropdown";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";
import { useCategoryLabel } from "@/i18n/use-category-label";
import { useResourceFilterDraft } from "./resource-filter-draft-context";
import { IntakeSignalFilters } from "./intake-signal-filters";
import {
  useResourceFilterOptions,
  formatFilterOptionLabel,
  type ResourceFilterOptions,
} from "./use-resource-filter-options";

interface ResourceFiltersProps {
  states: string[];
  globalOptions: ResourceFilterOptions;
  appliedOptions: ResourceFilterOptions;
  embedded?: boolean;
  compact?: boolean;
}

export function ResourceFiltersBar({
  states,
  globalOptions,
  appliedOptions,
  embedded = false,
  compact = false,
}: ResourceFiltersProps) {
  const [isPending, startTransition] = useTransition();
  const { t } = useTranslations();
  const categoryLabel = useCategoryLabel();
  const { draft, applied, setField, apply, clear, hasDraftFilters, hasAppliedFilters } =
    useResourceFilterDraft();
  const { options, isLoading } = useResourceFilterOptions(
    {
      state: draft.state,
      county: draft.county,
      city: draft.city,
      category: draft.category,
      service: draft.service,
      intake: draft.intake,
    },
    globalOptions,
    appliedOptions
  );

  const needsDynamicOptions = Boolean(
    draft.state ||
      draft.county ||
      draft.city ||
      draft.category ||
      draft.service ||
      draft.intake.length > 0
  );
  const facetOptions = needsDynamicOptions ? options : globalOptions;

  const categoryOptions = facetOptions.categories;
  const serviceOptions = facetOptions.services;
  const categoryCounts = facetOptions.categoryCounts;
  const serviceCounts = facetOptions.serviceCounts;
  const intakeCounts = facetOptions.intakeCounts;
  const countyOptions = draft.state ? facetOptions.counties : [];
  const countyCounts = facetOptions.countyCounts;
  const cityOptions = draft.state && draft.county ? facetOptions.cities : [];
  const facetsLoading = needsDynamicOptions && isLoading;

  const selectedCategoryMeta = draft.category
    ? categoryOptions.find((category) => category.slug === draft.category)
    : undefined;
  const selectedCategoryLocalCount = draft.category
    ? categoryCounts[draft.category] ?? 0
    : 0;
  const showCategoryNoLocalHint =
    Boolean(draft.county && draft.category && !facetsLoading) &&
    (selectedCategoryLocalCount === 0 || !selectedCategoryMeta);

  useEffect(() => {
    if (!draft.state || facetsLoading) return;
    if (draft.county && !countyOptions.includes(draft.county)) {
      setField("county", "");
    }
  }, [countyOptions, draft.county, draft.state, facetsLoading, setField]);

  useEffect(() => {
    if (facetsLoading) return;
    if (draft.county) return;
    if (draft.category && !categoryOptions.some((category) => category.slug === draft.category)) {
      setField("category", "");
    }
  }, [categoryOptions, draft.category, draft.county, facetsLoading, setField]);

  useEffect(() => {
    if (facetsLoading) return;
    if (draft.service && !serviceOptions.includes(draft.service)) {
      setField("service", "");
    }
  }, [draft.service, serviceOptions, facetsLoading, setField]);

  useEffect(() => {
    if (facetsLoading) return;
    if (draft.city && !cityOptions.includes(draft.city)) {
      setField("city", "");
    }
  }, [cityOptions, draft.city, facetsLoading, setField]);

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
      aria-busy={facetsLoading}
    >
      {facetsLoading ? (
        <div
          role="status"
          aria-live="polite"
          className="flex items-center gap-2 rounded-lg border border-border bg-muted/60 px-3 py-2 text-sm text-muted-foreground"
        >
          <Loader2 className="h-4 w-4 shrink-0 animate-spin text-primary" aria-hidden="true" />
          <span>{t("resources.filtersUpdating")}</span>
        </div>
      ) : null}

      <div
        className={cn(
          "space-y-4 transition-opacity duration-200",
          facetsLoading && "pointer-events-none opacity-60"
        )}
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
            ...categoryOptions.map((category) => ({
              value: category.slug,
              label: formatFilterOptionLabel(
                categoryLabel(category),
                categoryCounts[category.slug]
              ),
            })),
          ]}
          searchPlaceholder={t("resources.searchCategories")}
          disabled={facetsLoading}
        />
        {showCategoryNoLocalHint ? (
          <p
            className={cn(
              "text-sm text-muted-foreground",
              compact ? "sm:col-span-2 lg:col-span-3" : "md:col-span-2 xl:col-span-3"
            )}
          >
            {t("resources.categoryNoLocalInCounty", {
              county: draft.county,
              category: selectedCategoryMeta
                ? categoryLabel(selectedCategoryMeta)
                : draft.category,
            })}
          </p>
        ) : null}
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
          options={[
            { value: "", label: t("resources.allCounties") },
            ...countyOptions.map((county) => ({
              value: county,
              label: formatFilterOptionLabel(county, countyCounts[county]),
            })),
          ]}
          searchPlaceholder={t("resources.searchCounties")}
          disabled={!draft.state || facetsLoading}
        />
        <p
          className={cn(
            "text-sm text-muted-foreground",
            compact ? "sm:col-span-2 lg:col-span-3" : "md:col-span-2 xl:col-span-3"
          )}
        >
          {t("resources.countyFilterHint")}
        </p>
        {draft.county && !facetsLoading ? (
          <p
            className={cn(
              "text-sm text-muted-foreground",
              compact ? "sm:col-span-2 lg:col-span-3" : "md:col-span-2 xl:col-span-3"
            )}
          >
            {serviceOptions.length === 0
              ? t("resources.countyScopedServicesEmpty", { county: draft.county })
              : t("resources.countyScopedFiltersHint", { county: draft.county })}
          </p>
        ) : null}
        <Dropdown
          label={t("resources.city")}
          placeholder={t("resources.allCities")}
          value={draft.city}
          onChange={(value) => setField("city", value)}
          options={withPlaceholder(cityOptions, t("resources.allCities"))}
          searchPlaceholder={t("resources.searchCities")}
          disabled={!draft.county || facetsLoading || cityOptions.length === 0}
        />
        <Dropdown
          label={t("resources.serviceType")}
          placeholder={t("resources.allServices")}
          value={draft.service}
          onChange={(value) => setField("service", value)}
          options={[
            { value: "", label: t("resources.allServices") },
            ...serviceOptions.map((service) => ({
              value: service,
              label: formatFilterOptionLabel(service, serviceCounts[service]),
            })),
          ]}
          searchPlaceholder={t("resources.searchServices")}
          disabled={facetsLoading}
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

      <IntakeSignalFilters
        intakeCounts={intakeCounts}
        isLoading={facetsLoading}
      />
      </div>

      <div className="flex flex-col items-end gap-3 sm:flex-row sm:justify-end sm:gap-3">
        <Button
          type="button"
          variant="outline"
          className={cn(
            "h-12 w-auto max-w-full whitespace-nowrap",
            !(hasDraftFilters || hasAppliedFilters) &&
              "hidden sm:inline-flex sm:invisible sm:pointer-events-none"
          )}
          onClick={handleClear}
          disabled={isPending || !(hasDraftFilters || hasAppliedFilters)}
          aria-hidden={!(hasDraftFilters || hasAppliedFilters)}
          tabIndex={hasDraftFilters || hasAppliedFilters ? 0 : -1}
        >
          <X className="h-5 w-5 shrink-0" aria-hidden="true" />
          {t("resources.clearFilters")}
        </Button>
        <Button
          type="button"
          className="h-12 w-auto max-w-full whitespace-nowrap border-2 border-transparent"
          onClick={handleApply}
          loading={isPending}
        >
          <Search className="h-5 w-5 shrink-0" aria-hidden="true" />
          {t("resources.searchButton")}
        </Button>
      </div>
    </div>
  );
}
