"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useTransition } from "react";
import { X } from "lucide-react";
import { Dropdown } from "@/components/ui/dropdown";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { Category } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

interface ResourceFiltersProps {
  categories: Category[];
  states: string[];
  counties: string[];
  cities: string[];
  services: string[];
  embedded?: boolean;
}

export function ResourceFiltersBar({
  categories,
  states,
  counties,
  cities,
  services,
  embedded = false,
}: ResourceFiltersProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();
  const { t } = useTranslations();

  const updateParams = useCallback(
    (key: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      if (key === "state") {
        params.delete("county");
        params.delete("city");
      }
      if (key === "county") {
        params.delete("city");
      }
      startTransition(() => {
        router.push(`/resources?${params.toString()}`, { scroll: false });
      });
    },
    [router, searchParams]
  );

  const clearFilters = () => {
    startTransition(() => {
      router.push("/resources", { scroll: false });
    });
  };

  const hasFilters = searchParams.toString().length > 0;
  const selectedState = searchParams.get("state") ?? "";

  const withPlaceholder = (items: string[], placeholder: string) => [
    { value: "", label: placeholder },
    ...items.map((item) => ({ value: item, label: item })),
  ];

  const categoryLabel = (category: Category) => {
    const key = `categories.${category.slug}.name`;
    const translated = t(key);
    return translated === key ? category.name : translated;
  };

  return (
    <div
      className={cn(
        "w-full min-w-0 max-w-full",
        embedded ? "space-y-4" : "space-y-4 rounded-xl border border-border bg-card p-4 sm:p-6"
      )}
      role="group"
      aria-label={t("resources.filterAria")}
    >
      <div className="grid min-w-0 grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <Dropdown
          label={t("resources.category")}
          placeholder={t("resources.allCategories")}
          value={searchParams.get("category") ?? ""}
          onChange={(value) => updateParams("category", value)}
          options={[
            { value: "", label: t("resources.allCategories") },
            ...categories.map((c) => ({ value: c.slug, label: categoryLabel(c) })),
          ]}
          searchPlaceholder={t("resources.searchCategories")}
        />
        <Dropdown
          label={t("resources.state")}
          placeholder={t("resources.allStates")}
          value={selectedState}
          onChange={(value) => updateParams("state", value)}
          options={withPlaceholder(states, t("resources.allStates"))}
          searchPlaceholder={t("resources.searchStates")}
        />
        <Dropdown
          label={t("resources.county")}
          placeholder={t("resources.allCounties")}
          value={searchParams.get("county") ?? ""}
          onChange={(value) => updateParams("county", value)}
          options={withPlaceholder(counties, t("resources.allCounties"))}
          disabled={!selectedState}
          searchPlaceholder={t("resources.searchCounties")}
        />
        <Dropdown
          label={t("resources.city")}
          placeholder={t("resources.allCities")}
          value={searchParams.get("city") ?? ""}
          onChange={(value) => updateParams("city", value)}
          options={withPlaceholder(cities, t("resources.allCities"))}
          searchPlaceholder={t("resources.searchCities")}
        />
        <Dropdown
          label={t("resources.serviceType")}
          placeholder={t("resources.allServices")}
          value={searchParams.get("service") ?? ""}
          onChange={(value) => updateParams("service", value)}
          options={withPlaceholder(services, t("resources.allServices"))}
          searchPlaceholder={t("resources.searchServices")}
        />
        <Dropdown
          label={t("resources.sortFilter")}
          placeholder={t("common.default")}
          value={searchParams.get("filter") ?? ""}
          onChange={(value) => updateParams("filter", value)}
          searchable={false}
          options={[
            { value: "", label: t("common.default") },
            { value: "recent", label: t("resources.recentlyAdded") },
          ]}
        />
      </div>

      {hasFilters && (
        <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap">
          <Button
            variant="outline"
            className="w-full sm:w-auto"
            onClick={clearFilters}
            disabled={isPending}
          >
            <X className="h-5 w-5" aria-hidden="true" />
            {t("resources.clearFilters")}
          </Button>
        </div>
      )}
    </div>
  );
}
