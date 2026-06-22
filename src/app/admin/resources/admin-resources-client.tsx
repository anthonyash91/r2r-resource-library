"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Plus, Download, Upload, Pencil, Archive, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CategoryBadge } from "@/components/resources/category-badge";
import { Card } from "@/components/ui/card";
import type { Resource } from "@/types";
import { formatDate, cn } from "@/lib/utils";
import { MAX_FEATURED_RESOURCES } from "@/lib/featured-resources-storage";
import { archiveResourceById, setResourceFeatured } from "@/lib/admin-resources";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";
import { useConfirmDialog } from "@/components/ui/confirm-dialog";

interface AdminResourcesClientProps {
  initialResources: Resource[];
}

export function AdminResourcesClient({ initialResources }: AdminResourcesClientProps) {
  const router = useRouter();
  const { t, locale } = useTranslations();
  const { confirm, alert } = useConfirmDialog();
  const [resources, setResources] = useState(initialResources);
  const [busyId, setBusyId] = useState<string | null>(null);

  useEffect(() => {
    setResources(initialResources);
  }, [initialResources]);

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(resources, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `resources-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (isSupabaseConfigured()) {
      await alert({ title: t("common.notice"), message: t("admin.importDbUnavailable") });
      e.target.value = "";
      return;
    }

    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async (ev) => {
      try {
        const imported = JSON.parse(ev.target?.result as string) as Resource[];
        setResources((prev) => [...prev, ...imported]);
        await alert({
          title: t("common.success"),
          message: t("admin.importSuccess", { count: imported.length }),
        });
      } catch {
        await alert({ title: t("common.error"), message: t("admin.importInvalid") });
      }
    };
    reader.readAsText(file);
  };

  const archiveResource = async (id: string) => {
    const confirmed = await confirm({
      title: t("admin.archive"),
      message: t("admin.archiveConfirm"),
      confirmLabel: t("admin.archive"),
      destructive: true,
    });
    if (!confirmed) return;

    if (isSupabaseConfigured()) {
      setBusyId(id);
      const result = await archiveResourceById(id);
      setBusyId(null);
      if (result.error) {
        await alert({ title: t("common.error"), message: t("admin.resourceSaveFailed") });
        return;
      }
      router.refresh();
    }

    setResources((prev) =>
      prev.map((r) =>
        r.id === id ? { ...r, status: "archived" as const, is_featured: false } : r
      )
    );
  };

  const toggleFeatured = async (resource: Resource) => {
    const nextFeatured = !resource.is_featured;

    if (isSupabaseConfigured()) {
      setBusyId(resource.id);
      const result = await setResourceFeatured(resource.id, nextFeatured, resource.is_featured);
      setBusyId(null);

      if (result.error === "max_featured") {
        await alert({
          title: t("common.notice"),
          message: t("admin.featuredMaxAlert", { max: MAX_FEATURED_RESOURCES }),
        });
        return;
      }
      if (result.error) {
        await alert({ title: t("common.error"), message: t("admin.resourceSaveFailed") });
        return;
      }
      router.refresh();
    }

    setResources((prev) =>
      prev.map((r) => (r.id === resource.id ? { ...r, is_featured: nextFeatured } : r))
    );
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
                {resource.is_featured && (
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
                  variant={resource.is_featured ? "primary" : "outline"}
                  size="sm"
                  onClick={() => toggleFeatured(resource)}
                  disabled={busyId === resource.id}
                  aria-pressed={resource.is_featured}
                  aria-label={
                    resource.is_featured
                      ? t("admin.removeFeatured")
                      : t("admin.featureOnHomepage")
                  }
                >
                  <Star
                    className={cn("h-4 w-4", resource.is_featured && "fill-current")}
                    aria-hidden="true"
                  />
                  {resource.is_featured ? t("admin.featured") : t("admin.feature")}
                </Button>
              )}
              <Link href={`/admin/resources/${resource.id}/edit`}>
                <Button variant="outline" size="sm">
                  <Pencil className="h-4 w-4" aria-hidden="true" />
                  {t("admin.edit")}
                </Button>
              </Link>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => archiveResource(resource.id)}
                disabled={busyId === resource.id}
              >
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
