"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Dropdown } from "@/components/ui/dropdown";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import type { Category } from "@/types";
import { MAX_FEATURED_RESOURCES } from "@/lib/featured-resources-storage";
import {
  createResource,
  updateResource,
  type ResourceFormData,
} from "@/lib/admin-resources";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

interface ResourceFormProps {
  categories: Category[];
  resource?: ResourceFormData & { id?: string };
}

export function ResourceForm({ categories, resource }: ResourceFormProps) {
  const router = useRouter();
  const { t } = useTranslations();
  const [form, setForm] = useState<ResourceFormData>({
    name: resource?.name ?? "",
    description: resource?.description ?? "",
    category_id: resource?.category_id ?? categories[0]?.id ?? "",
    state: resource?.state ?? "",
    county: resource?.county ?? "",
    city: resource?.city ?? "",
    address: resource?.address ?? "",
    phone: resource?.phone ?? "",
    website: resource?.website ?? "",
    email: resource?.email ?? "",
    hours: resource?.hours ?? "",
    eligibility: resource?.eligibility ?? "",
    notes: resource?.notes ?? "",
    services: resource?.services ?? "",
    tags: resource?.tags ?? "",
    status: resource?.status ?? "active",
    is_featured: resource?.is_featured ?? false,
  });
  const [saving, setSaving] = useState(false);
  const wasFeatured = resource?.is_featured ?? false;

  const update = (key: keyof ResourceFormData, value: string | boolean) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    if (!isSupabaseConfigured()) {
      alert(t("admin.resourceSaveFailed"));
      setSaving(false);
      return;
    }

    if (resource?.id) {
      const result = await updateResource(resource.id, form, wasFeatured);
      if (result.error === "max_featured") {
        alert(t("admin.featuredMaxAlert", { max: MAX_FEATURED_RESOURCES }));
        setForm((prev) => ({ ...prev, is_featured: wasFeatured }));
        setSaving(false);
        return;
      }
      if (result.error) {
        alert(t("admin.resourceSaveFailed"));
        setSaving(false);
        return;
      }
    } else {
      const result = await createResource(form);
      if (result.error === "max_featured") {
        alert(t("admin.featuredMaxAlert", { max: MAX_FEATURED_RESOURCES }));
        setForm((prev) => ({ ...prev, is_featured: false }));
        setSaving(false);
        return;
      }
      if (result.error) {
        alert(t("admin.resourceSaveFailed"));
        setSaving(false);
        return;
      }
    }

    setSaving(false);
    router.push("/admin/resources");
    router.refresh();
  };

  return (
    <Card>
      <form onSubmit={handleSubmit} className="space-y-6">
        <Input
          label={t("admin.resourceName")}
          value={form.name}
          onChange={(e) => update("name", e.target.value)}
          required
        />
        <div>
          <label htmlFor="description" className="mb-2 block text-base font-semibold">
            {t("admin.description")}
          </label>
          <textarea
            id="description"
            value={form.description}
            onChange={(e) => update("description", e.target.value)}
            required
            rows={5}
            className="w-full rounded-xl border-2 border-border bg-card px-4 py-3 text-base focus:border-primary focus:outline-none focus:ring-2 focus:ring-ring/30"
          />
        </div>
        <Dropdown
          label={t("admin.categoryLabel")}
          value={form.category_id}
          onChange={(value) => update("category_id", value)}
          options={categories.map((c) => ({ value: c.id, label: c.name }))}
        />
        <div className="grid gap-4 sm:grid-cols-3">
          <Input label={t("admin.stateLabel")} value={form.state} onChange={(e) => update("state", e.target.value)} />
          <Input label={t("admin.countyLabel")} value={form.county} onChange={(e) => update("county", e.target.value)} />
          <Input label={t("admin.cityLabel")} value={form.city} onChange={(e) => update("city", e.target.value)} />
        </div>
        <Input label={t("admin.address")} value={form.address} onChange={(e) => update("address", e.target.value)} />
        <div className="grid gap-4 sm:grid-cols-2">
          <Input label={t("admin.phone")} type="tel" value={form.phone} onChange={(e) => update("phone", e.target.value)} />
          <Input label={t("admin.email")} type="email" value={form.email} onChange={(e) => update("email", e.target.value)} />
        </div>
        <Input label={t("admin.website")} type="url" value={form.website} onChange={(e) => update("website", e.target.value)} />
        <Input label={t("admin.hours")} value={form.hours} onChange={(e) => update("hours", e.target.value)} />
        <div>
          <label htmlFor="eligibility" className="mb-2 block text-base font-semibold">
            {t("admin.eligibility")}
          </label>
          <textarea
            id="eligibility"
            value={form.eligibility}
            onChange={(e) => update("eligibility", e.target.value)}
            rows={3}
            className="w-full rounded-xl border-2 border-border bg-card px-4 py-3 text-base focus:border-primary focus:outline-none focus:ring-2 focus:ring-ring/30"
          />
          <p className="mt-1 text-sm text-muted-foreground">{t("admin.eligibilityHint")}</p>
        </div>
        <div>
          <label htmlFor="notes" className="mb-2 block text-base font-semibold">
            {t("admin.notes")}
          </label>
          <textarea
            id="notes"
            value={form.notes}
            onChange={(e) => update("notes", e.target.value)}
            rows={3}
            className="w-full rounded-xl border-2 border-border bg-card px-4 py-3 text-base focus:border-primary focus:outline-none focus:ring-2 focus:ring-ring/30"
          />
          <p className="mt-1 text-sm text-muted-foreground">{t("admin.notesHint")}</p>
        </div>
        <Input
          label={t("admin.services")}
          value={form.services}
          onChange={(e) => update("services", e.target.value)}
          hint={t("admin.servicesHint")}
        />
        <Input
          label={t("admin.tags")}
          value={form.tags}
          onChange={(e) => update("tags", e.target.value)}
        />
        <Dropdown
          label={t("admin.status")}
          value={form.status}
          onChange={(value) => update("status", value)}
          options={[
            { value: "active", label: t("common.active") },
            { value: "inactive", label: t("common.inactive") },
            { value: "archived", label: t("common.archived") },
          ]}
          searchable={false}
        />
        <label className="flex cursor-pointer items-start gap-3 rounded-xl border border-border px-4 py-4">
          <input
            type="checkbox"
            checked={form.is_featured}
            onChange={(e) => update("is_featured", e.target.checked)}
            className="mt-1 h-5 w-5 cursor-pointer accent-primary"
          />
          <span>
            <span className="block font-semibold">{t("admin.featureOnHomepage")}</span>
            <span className="block text-sm text-muted-foreground">
              {t("admin.featureOnHomepageDesc")}
            </span>
          </span>
        </label>
        <div className="flex gap-3">
          <Button type="submit" size="lg" disabled={saving}>
            {saving
              ? t("admin.saving")
              : resource?.id
                ? t("admin.updateResource")
                : t("admin.createResource")}
          </Button>
          <Button type="button" variant="outline" size="lg" onClick={() => router.back()}>
            {t("common.cancel")}
          </Button>
        </div>
      </form>
    </Card>
  );
}
