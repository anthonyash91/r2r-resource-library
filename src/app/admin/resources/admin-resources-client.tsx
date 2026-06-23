"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Plus,
  Download,
  Upload,
  Pencil,
  Archive,
  ArchiveRestore,
  Star,
  CheckCircle,
  CircleOff,
  LayoutList,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CategoryBadge } from "@/components/resources/category-badge";
import { Card } from "@/components/ui/card";
import type { Resource } from "@/types";
import { formatDate, cn } from "@/lib/utils";
import { MAX_FEATURED_RESOURCES } from "@/lib/featured-resources-storage";
import {
  archiveResourceById,
  setResourceFeatured,
  unarchiveResourceById,
} from "@/lib/admin-resources";
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
  const [showArchived, setShowArchived] = useState(false);

  useEffect(() => {
    setResources(initialResources);
  }, [initialResources]);

  const archivedCount = useMemo(
    () => resources.filter((resource) => resource.status === "archived").length,
    [resources]
  );

  const visibleResources = useMemo(
    () =>
      resources.filter((resource) =>
        showArchived ? resource.status === "archived" : resource.status !== "archived"
      ),
    [resources, showArchived]
  );

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

  const unarchiveResource = async (id: string) => {
    const confirmed = await confirm({
      title: t("admin.unarchive"),
      message: t("admin.unarchiveConfirm"),
      confirmLabel: t("admin.unarchive"),
    });
    if (!confirmed) return;

    if (isSupabaseConfigured()) {
      setBusyId(id);
      const result = await unarchiveResourceById(id);
      setBusyId(null);
      if (result.error) {
        await alert({ title: t("common.error"), message: t("admin.resourceSaveFailed") });
        return;
      }
      router.refresh();
    }

    setResources((prev) =>
      prev.map((r) => (r.id === id ? { ...r, status: "active" as const } : r))
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

  const statusBadge = (status: Resource["status"]) => {
    if (status === "active") {
      return (
        <Badge variant="success" icon={CheckCircle}>
          {t("common.active")}
        </Badge>
      );
    }
    if (status === "inactive") {
      return (
        <Badge variant="default" icon={CircleOff}>
          {t("common.inactive")}
        </Badge>
      );
    }
    return (
      <Badge variant="default" icon={Archive}>
        {t("common.archived")}
      </Badge>
    );
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
          <label className="inline-flex min-h-[48px] cursor-pointer items-center justify-center gap-2 rounded-xl border-2 border-primary bg-transparent px-6 py-3 text-base font-semibold text-primary hover:bg-secondary">
            <Upload className="h-5 w-5" aria-hidden="true" />
            {t("admin.import")}
            <input type="file" accept=".json,.csv" className="hidden" onChange={handleImport} />
          </label>
        </div>
      </header>

      <div className="mb-6 flex flex-wrap items-center gap-2">
        <Button
          variant={showArchived ? "soft" : "soft-primary"}
          size="badge"
          onClick={() => setShowArchived(false)}
          aria-pressed={!showArchived}
        >
          <LayoutList className="h-3.5 w-3.5" aria-hidden="true" />
          {t("admin.showActiveResources")}
        </Button>
        <Button
          variant={showArchived ? "soft-primary" : "soft"}
          size="badge"
          onClick={() => setShowArchived(true)}
          aria-pressed={showArchived}
        >
          <Archive className="h-3.5 w-3.5" aria-hidden="true" />
          {t("admin.showArchivedResources")}
          {archivedCount > 0 ? ` (${archivedCount})` : ""}
        </Button>
      </div>

      {visibleResources.length === 0 ? (
        <p className="text-base text-muted-foreground">
          {showArchived ? t("admin.noArchivedResources") : t("admin.noActiveResources")}
        </p>
      ) : (
        <div className="space-y-4">
          {visibleResources.map((resource) => (
            <Card
              key={resource.id}
              className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
            >
              <div className="flex-1">
                <div className="mb-2 flex flex-wrap gap-2">
                  {resource.category && <CategoryBadge category={resource.category} />}
                  {resource.is_featured && !showArchived ? (
                    <Badge variant="warning" icon={Star}>
                      {t("admin.featured")}
                    </Badge>
                  ) : null}
                  {statusBadge(resource.status)}
                </div>
                <h2 className="text-lg font-bold">{resource.name}</h2>
                <p className="text-sm text-muted-foreground">
                  {[resource.city, resource.state].filter(Boolean).join(", ")} ·{" "}
                  {formatDate(resource.updated_at, locale)}
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {!showArchived && resource.status === "active" ? (
                  <Button
                    variant={resource.is_featured ? "soft-warning" : "soft-primary"}
                    size="badge"
                    onClick={() => toggleFeatured(resource)}
                    loading={busyId === resource.id}
                    aria-pressed={resource.is_featured}
                    aria-label={
                      resource.is_featured
                        ? t("admin.removeFeatured")
                        : t("admin.featureOnHomepage")
                    }
                  >
                    <Star
                      className={cn("h-3.5 w-3.5", resource.is_featured && "fill-current")}
                      aria-hidden="true"
                    />
                    {resource.is_featured ? t("admin.featured") : t("admin.feature")}
                  </Button>
                ) : null}
                <Link href={`/admin/resources/${resource.id}/edit`}>
                  <Button variant="soft-accent" size="badge">
                    <Pencil className="h-3.5 w-3.5" aria-hidden="true" />
                    {t("admin.edit")}
                  </Button>
                </Link>
                {showArchived ? (
                  <Button
                    variant="soft-success"
                    size="badge"
                    onClick={() => unarchiveResource(resource.id)}
                    loading={busyId === resource.id}
                  >
                    <ArchiveRestore className="h-3.5 w-3.5" aria-hidden="true" />
                    {t("admin.unarchive")}
                  </Button>
                ) : (
                  <Button
                    variant="soft-warning"
                    size="badge"
                    onClick={() => archiveResource(resource.id)}
                    loading={busyId === resource.id}
                  >
                    <Archive className="h-3.5 w-3.5" aria-hidden="true" />
                    {t("admin.archive")}
                  </Button>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
