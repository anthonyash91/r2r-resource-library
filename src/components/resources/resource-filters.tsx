"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useRef, useTransition } from "react";
import { Search, X } from "lucide-react";
import { SearchField } from "@/components/ui/search-field";
import { Dropdown } from "@/components/ui/dropdown";
import { Button } from "@/components/ui/button";
import type { Category } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

interface ResourceFiltersProps {
  categories: Category[];
  states: string[];
  counties: string[];
  cities: string[];
  services: string[];
  hideCategory?: boolean;
  embedded?: boolean;
}

export function ResourceFiltersBar({
  categories,
  states,
  counties,
  cities,
  services,
  hideCategory = false,
  embedded = false,
}: ResourceFiltersProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();
  const searchRef = useRef<HTMLInputElement>(null);
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
        router.push(`/resources?${params.toString()}`);
      });
    },
    [router, searchParams]
  );

  const clearFilters = () => {
    startTransition(() => {
      router.push("/resources");
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
      className={embedded ? "space-y-4" : "space-y-4 rounded-2xl border border-border bg-card p-6"}
      role="search"
      aria-label={t("resources.filterAria")}
    >
      <SearchField
        ref={searchRef}
        label={t("resources.searchKeyword")}
        placeholder={t("resources.searchKeywordPlaceholder")}
        defaultValue={searchParams.get("q") ?? ""}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            updateParams("q", (e.target as HTMLInputElement).value);
          }
        }}
        aria-label={t("resources.searchKeyword")}
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {!hideCategory && (
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
        )}
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

      <div className="flex flex-wrap gap-3">
        <Button
          onClick={() => updateParams("q", searchRef.current?.value ?? searchParams.get("q") ?? "")}
          disabled={isPending}
        >
          <Search className="h-5 w-5" aria-hidden="true" />
          {t("resources.searchButton")}
        </Button>
        {hasFilters && (
          <Button variant="outline" onClick={clearFilters} disabled={isPending}>
            <X className="h-5 w-5" aria-hidden="true" />
            {t("resources.clearFilters")}
          </Button>
        )}
      </div>
    </div>
  );
}
