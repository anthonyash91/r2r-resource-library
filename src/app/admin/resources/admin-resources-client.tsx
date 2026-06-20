"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Plus, Download, Upload, Pencil, Archive, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CategoryBadge } from "@/components/resources/category-badge";
import { Card } from "@/components/ui/card";
import type { Resource } from "@/types";
import { formatDate, cn } from "@/lib/utils";
import {
  getFeaturedIdsFromResources,
  MAX_FEATURED_RESOURCES,
  toggleStoredFeaturedId,
} from "@/lib/featured-resources-storage";
import { useTranslations } from "@/i18n/locale-context";

interface AdminResourcesClientProps {
  initialResources: Resource[];
}

export function AdminResourcesClient({ initialResources }: AdminResourcesClientProps) {
  const { t, locale } = useTranslations();
  const [resources, setResources] = useState(initialResources);
  const [featuredIds, setFeaturedIds] = useState<string[]>(() =>
    getFeaturedIdsFromResources(initialResources.filter((resource) => resource.status === "active"))
  );

  useEffect(() => {
    const syncFeatured = () => {
      setFeaturedIds(
        getFeaturedIdsFromResources(resources.filter((resource) => resource.status === "active"))
      );
    };

    syncFeatured();
    window.addEventListener("featured-resources-updated", syncFeatured);
    window.addEventListener("storage", syncFeatured);

    return () => {
      window.removeEventListener("featured-resources-updated", syncFeatured);
      window.removeEventListener("storage", syncFeatured);
    };
  }, [resources]);

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(resources, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `resources-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const imported = JSON.parse(ev.target?.result as string) as Resource[];
        setResources((prev) => [...prev, ...imported]);
        alert(t("admin.importSuccess", { count: imported.length }));
      } catch {
        alert(t("admin.importInvalid"));
      }
    };
    reader.readAsText(file);
  };

  const archiveResource = (id: string) => {
    if (!confirm(t("admin.archiveConfirm"))) return;
    setResources((prev) =>
      prev.map((r) => (r.id === id ? { ...r, status: "archived" as const } : r))
    );
  };

  const toggleFeatured = (resource: Resource) => {
    const activeResources = resources.filter((item) => item.status === "active");
    const nextIds = toggleStoredFeaturedId(activeResources, resource.id);
    if (nextIds === featuredIds && !featuredIds.includes(resource.id)) {
      alert(t("admin.featuredMaxAlert", { max: MAX_FEATURED_RESOURCES }));
      return;
    }
    setFeaturedIds(nextIds);
  };

  const statusLabel = (status: string) => {
    if (status === "active") return t("common.active");
    if (status === "inactive") return t("common.inactive");
    if (status === "archived") return t("common.archived");
    return status;
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.resourceManagement")}</h1>
          <p className="text-lg text-muted-foreground">{t("admin.resourceManagementDesc")}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/admin/resources/new">
            <Button>
              <Plus className="h-5 w-5" aria-hidden="true" />
              {t("admin.addResource")}
            </Button>
          </Link>
          <Button variant="outline" onClick={handleExport}>
            <Download className="h-5 w-5" aria-hidden="true" />
            {t("admin.export")}
          </Button>
          <label className="inline-flex cursor-pointer items-center justify-center gap-2 rounded-xl border-2 border-primary bg-transparent px-6 py-3 text-base font-semibold text-primary hover:bg-secondary min-h-[48px]">
            <Upload className="h-5 w-5" aria-hidden="true" />
            {t("admin.import")}
            <input type="file" accept=".json,.csv" className="hidden" onChange={handleImport} />
          </label>
        </div>
      </header>

      <div className="space-y-4">
        {resources.filter((r) => r.status !== "archived").map((resource) => (
          <Card key={resource.id} className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex-1">
              <div className="mb-2 flex flex-wrap gap-2">
                {resource.category && <CategoryBadge category={resource.category} />}
                {featuredIds.includes(resource.id) && (
                  <Badge variant="warning">{t("admin.featured")}</Badge>
                )}
                <Badge variant={resource.status === "active" ? "success" : "default"}>
                  {statusLabel(resource.status)}
                </Badge>
              </div>
              <h2 className="text-lg font-bold">{resource.name}</h2>
              <p className="text-sm text-muted-foreground">
                {[resource.city, resource.state].filter(Boolean).join(", ")} ·{" "}
                {formatDate(resource.updated_at, locale)}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {resource.status === "active" && (
                <Button
                  variant={featuredIds.includes(resource.id) ? "primary" : "outline"}
                  size="sm"
                  onClick={() => toggleFeatured(resource)}
                  aria-pressed={featuredIds.includes(resource.id)}
                  aria-label={
                    featuredIds.includes(resource.id)
                      ? t("admin.removeFeatured")
                      : t("admin.featureOnHomepage")
                  }
                >
                  <Star
                    className={cn("h-4 w-4", featuredIds.includes(resource.id) && "fill-current")}
                    aria-hidden="true"
                  />
                  {featuredIds.includes(resource.id) ? t("admin.featured") : t("admin.feature")}
                </Button>
              )}
              <Link href={`/admin/resources/${resource.id}/edit`}>
                <Button variant="outline" size="sm">
                  <Pencil className="h-4 w-4" aria-hidden="true" />
                  {t("admin.edit")}
                </Button>
              </Link>
              <Button variant="ghost" size="sm" onClick={() => archiveResource(resource.id)}>
                <Archive className="h-4 w-4" aria-hidden="true" />
                {t("admin.archive")}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
