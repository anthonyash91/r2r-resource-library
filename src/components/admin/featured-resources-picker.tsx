"use client";

import { useEffect, useMemo, useState } from "react";
import { Search, Star, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { CategoryBadge } from "@/components/resources/category-badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import type { Resource } from "@/types";
import {
  getFeaturedIdsFromResources,
  MAX_FEATURED_RESOURCES,
  setStoredFeaturedIds,
  toggleStoredFeaturedId,
} from "@/lib/featured-resources-storage";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";

interface FeaturedResourcesPickerProps {
  resources: Resource[];
}

export function FeaturedResourcesPicker({ resources }: FeaturedResourcesPickerProps) {
  const { t } = useTranslations();
  const activeResources = useMemo(
    () => resources.filter((resource) => resource.status === "active"),
    [resources]
  );
  const [featuredIds, setFeaturedIds] = useState<string[]>(() =>
    getFeaturedIdsFromResources(activeResources)
  );
  const [query, setQuery] = useState("");

  useEffect(() => {
    const syncFeatured = () => {
      setFeaturedIds(getFeaturedIdsFromResources(activeResources));
    };

    syncFeatured();
    window.addEventListener("featured-resources-updated", syncFeatured);
    window.addEventListener("storage", syncFeatured);

    return () => {
      window.removeEventListener("featured-resources-updated", syncFeatured);
      window.removeEventListener("storage", syncFeatured);
    };
  }, [activeResources]);

  const featuredResources = featuredIds
    .map((id) => activeResources.find((resource) => resource.id === id))
    .filter((resource): resource is Resource => Boolean(resource));

  const availableResources = activeResources.filter(
    (resource) =>
      !featuredIds.includes(resource.id) &&
      (query.trim() === "" ||
        resource.name.toLowerCase().includes(query.toLowerCase()) ||
        resource.category?.name.toLowerCase().includes(query.toLowerCase()))
  );

  const handleToggle = (id: string) => {
    const nextIds = toggleStoredFeaturedId(activeResources, id);
    if (nextIds === featuredIds && !featuredIds.includes(id)) {
      alert(t("admin.featuredMaxAlert", { max: MAX_FEATURED_RESOURCES }));
      return;
    }
    setFeaturedIds(nextIds);
  };

  const handleRemove = (id: string) => {
    const nextIds = featuredIds.filter((featuredId) => featuredId !== id);
    setStoredFeaturedIds(nextIds);
    setFeaturedIds(nextIds);
  };

  return (
    <Card className="space-y-6">
      <div>
        <h2 className="text-xl font-bold">{t("admin.featuredResources")}</h2>
        <p className="mt-1 text-base text-muted-foreground">
          {t("admin.featuredResourcesDesc", { max: MAX_FEATURED_RESOURCES })}
        </p>
      </div>

      <div>
        <p className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          {t("admin.currentlyFeatured")} ({featuredResources.length}/{MAX_FEATURED_RESOURCES})
        </p>
        {featuredResources.length === 0 ? (
          <p className="rounded-xl border border-dashed border-border px-4 py-6 text-center text-muted-foreground">
            {t("admin.noFeatured")}
          </p>
        ) : (
          <ul className="space-y-3">
            {featuredResources.map((resource) => (
              <li
                key={resource.id}
                className="flex items-center justify-between gap-3 rounded-xl border border-border bg-muted/40 px-4 py-3"
              >
                <div className="min-w-0">
                  <div className="mb-1 flex flex-wrap items-center gap-2">
                    {resource.category && <CategoryBadge category={resource.category} />}
                    <Badge variant="warning">{t("admin.featured")}</Badge>
                  </div>
                  <p className="truncate font-semibold">{resource.name}</p>
                  <p className="truncate text-sm text-muted-foreground">
                    {[resource.city, resource.state].filter(Boolean).join(", ")}
                  </p>
                </div>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => handleRemove(resource.id)}
                  aria-label={t("admin.removeFeatured")}
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                  {t("common.remove")}
                </Button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <label htmlFor="featured-search" className="mb-2 block font-semibold">
          {t("admin.addResourceSearch")}
        </label>
        <div className="relative mb-4">
          <Search
            className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground"
            aria-hidden="true"
          />
          <input
            id="featured-search"
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t("admin.addResourceSearch")}
            className="w-full rounded-xl border-2 border-border bg-card py-3 pl-12 pr-4 text-base focus:border-primary focus:outline-none focus:ring-2 focus:ring-ring/30"
          />
        </div>

        <ul className="max-h-80 space-y-2 overflow-y-auto">
          {availableResources.slice(0, 20).map((resource) => (
            <li key={resource.id}>
              <button
                type="button"
                onClick={() => handleToggle(resource.id)}
                disabled={featuredIds.length >= MAX_FEATURED_RESOURCES}
                className={cn(
                  "flex w-full cursor-pointer items-center justify-between gap-3 rounded-xl border border-border px-4 py-3 text-left transition-colors hover:bg-secondary",
                  "disabled:cursor-not-allowed disabled:opacity-50"
                )}
              >
                <div className="min-w-0">
                  <p className="truncate font-semibold">{resource.name}</p>
                  <p className="truncate text-sm text-muted-foreground">
                    {resource.category?.name}
                    {[resource.city, resource.state].filter(Boolean).length > 0 && " · "}
                    {[resource.city, resource.state].filter(Boolean).join(", ")}
                  </p>
                </div>
                <Star className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
              </button>
            </li>
          ))}
          {availableResources.length === 0 && (
            <li className="rounded-xl border border-dashed border-border px-4 py-6 text-center text-muted-foreground">
              {t("admin.noMatchingResources")}
            </li>
          )}
        </ul>
      </div>
    </Card>
  );
}
