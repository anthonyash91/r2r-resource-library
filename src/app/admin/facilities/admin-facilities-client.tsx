"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, Eye, Trash2, CheckCircle, CircleOff, Save, X, Power, PowerOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useTranslations } from "@/i18n/locale-context";
import { useConfirmDialog } from "@/components/ui/confirm-dialog";

export interface AdminFacilityRow {
  id: string;
  name: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
  siteIdMasked: string;
  signupCount: number;
}

interface AdminFacilitiesClientProps {
  initialFacilities: AdminFacilityRow[];
}

export function AdminFacilitiesClient({ initialFacilities }: AdminFacilitiesClientProps) {
  const { t } = useTranslations();
  const { alert, confirm } = useConfirmDialog();
  const router = useRouter();
  const [facilities, setFacilities] = useState(initialFacilities);
  const [showNew, setShowNew] = useState(false);
  const [saving, setSaving] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [form, setForm] = useState({ name: "", siteId: "" });
  const [createdSiteId, setCreatedSiteId] = useState<string | null>(null);

  const resetForm = () => {
    setForm({ name: "", siteId: "" });
    setShowNew(false);
    setCreatedSiteId(null);
  };

  const handleCreate = async () => {
    const name = form.name.trim();
    const siteId = form.siteId.trim();
    if (!name || !siteId) return;

    setSaving(true);
    const res = await fetch("/api/admin/facilities", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, siteId }),
    });

    if (!res.ok) {
      const payload = (await res.json().catch(() => ({}))) as { error?: string };
      await alert({
        title: t("common.error"),
        message: payload.error ?? t("admin.facilitySaveFailed"),
      });
      setSaving(false);
      return;
    }

    const payload = (await res.json()) as {
      facility: AdminFacilityRow & { siteId?: string };
    };

    setFacilities((prev) => [
      ...prev,
      {
        id: payload.facility.id,
        name: payload.facility.name,
        isActive: payload.facility.isActive,
        createdAt: payload.facility.createdAt,
        updatedAt: payload.facility.updatedAt,
        siteIdMasked: `••••${siteId.slice(-4)}`,
        signupCount: 0,
      },
    ]);
    setCreatedSiteId(siteId);
    setForm({ name: "", siteId: "" });
    setSaving(false);
    router.refresh();
  };

  const toggleActive = async (facility: AdminFacilityRow) => {
    setBusyId(facility.id);
    const res = await fetch(`/api/admin/facilities/${facility.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ isActive: !facility.isActive }),
    });

    if (!res.ok) {
      await alert({ title: t("common.error"), message: t("admin.facilitySaveFailed") });
      setBusyId(null);
      return;
    }

    setFacilities((prev) =>
      prev.map((item) =>
        item.id === facility.id ? { ...item, isActive: !item.isActive } : item
      )
    );
    setBusyId(null);
    router.refresh();
  };

  const handleDelete = async (facility: AdminFacilityRow) => {
    const message =
      facility.signupCount > 0
        ? t("admin.facilityDeleteWithAccountsConfirm", {
            name: facility.name,
            count: String(facility.signupCount),
          })
        : t("admin.facilityDeleteConfirm", { name: facility.name });

    const confirmed = await confirm({
      title: t("admin.facilityDelete"),
      message,
      confirmLabel: t("admin.facilityDelete"),
      destructive: true,
    });
    if (!confirmed) return;

    setBusyId(facility.id);
    const res = await fetch(`/api/admin/facilities/${facility.id}`, { method: "DELETE" });

    if (!res.ok) {
      const payload = (await res.json().catch(() => ({}))) as { error?: string };
      await alert({
        title: t("common.error"),
        message: payload.error ?? t("admin.facilityDeleteFailed"),
      });
      setBusyId(null);
      return;
    }

    setFacilities((prev) => prev.filter((item) => item.id !== facility.id));
    setBusyId(null);
    router.refresh();
  };

  const revealSiteId = async (facilityId: string) => {
    setBusyId(facilityId);
    const res = await fetch(`/api/admin/facilities/${facilityId}`);
    if (!res.ok) {
      await alert({ title: t("common.error"), message: t("admin.facilityNotFound") });
      setBusyId(null);
      return;
    }
    const payload = (await res.json()) as { siteId?: string };
    if (!payload.siteId) {
      await alert({ title: t("common.error"), message: t("admin.facilityNotFound") });
      setBusyId(null);
      return;
    }
    await navigator.clipboard.writeText(payload.siteId);
    setBusyId(null);
    await alert({
      title: t("common.success"),
      message: `${t("admin.facilitySiteIdCopied")} (${payload.siteId})`,
    });
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.facilitiesTitle")}</h1>
          <p className="text-lg text-muted-foreground">{t("admin.facilitiesDesc")}</p>
        </div>
        <Button onClick={() => setShowNew(true)} disabled={showNew}>
          <Plus className="h-4 w-4" aria-hidden="true" />
          {t("admin.facilityAdd")}
        </Button>
      </header>

      {showNew ? (
        <Card className="mb-8 space-y-4">
          <Input
            label={t("admin.facilityNameLabel")}
            value={form.name}
            onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))}
          />
          <Input
            label={t("admin.facilitySiteIdLabel")}
            value={form.siteId}
            onChange={(e) => setForm((prev) => ({ ...prev, siteId: e.target.value }))}
            hint={t("admin.facilitySiteIdHint")}
          />
          {createdSiteId ? (
            <p className="rounded-lg border border-primary/30 bg-primary/5 p-4 text-base">
              {t("admin.facilityCreatedSiteIdNote", { siteId: createdSiteId })}
            </p>
          ) : null}
          <div className="flex flex-wrap gap-2">
            <Button onClick={handleCreate} loading={saving}>
              <Save className="h-4 w-4" aria-hidden="true" />
              {t("common.save")}
            </Button>
            <Button variant="outline" onClick={resetForm} disabled={saving}>
              <X className="h-4 w-4" aria-hidden="true" />
              {t("common.cancel")}
            </Button>
          </div>
        </Card>
      ) : null}

      <div className="space-y-4">
        {facilities.map((facility) => (
          <Card key={facility.id} className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="mb-2 flex flex-wrap items-center gap-2">
                <h2 className="text-xl font-bold">{facility.name}</h2>
                <Badge
                  variant={facility.isActive ? "success" : "secondary"}
                  icon={facility.isActive ? CheckCircle : CircleOff}
                >
                  {facility.isActive ? t("admin.facilityActive") : t("admin.facilityInactive")}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">
                {t("admin.facilitySiteIdMasked")}: {facility.siteIdMasked}
              </p>
              <p className="text-sm text-muted-foreground">
                {t("admin.facilitySignups")}: {facility.signupCount}
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <Button
                variant="soft-primary"
                size="badge"
                onClick={() => revealSiteId(facility.id)}
                loading={busyId === facility.id}
              >
                <Eye className="h-3.5 w-3.5" aria-hidden="true" />
                {t("admin.facilityRevealSiteId")}
              </Button>
              <Button
                variant={facility.isActive ? "soft-warning" : "soft-success"}
                size="badge"
                onClick={() => toggleActive(facility)}
                loading={busyId === facility.id}
              >
                {facility.isActive ? (
                  <PowerOff className="h-3.5 w-3.5" aria-hidden="true" />
                ) : (
                  <Power className="h-3.5 w-3.5" aria-hidden="true" />
                )}
                {facility.isActive ? t("admin.facilityDeactivate") : t("admin.facilityActivate")}
              </Button>
              <Button
                variant="soft-destructive"
                size="badge"
                onClick={() => handleDelete(facility)}
                loading={busyId === facility.id}
              >
                <Trash2 className="h-3.5 w-3.5" aria-hidden="true" />
                {t("admin.facilityDelete")}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
