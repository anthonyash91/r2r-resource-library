"use client";

import { useMemo, useState } from "react";
import { Plus, Pencil } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dropdown } from "@/components/ui/dropdown";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { CmsPage } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

const emptyForm = { title: "", slug: "", content: "", status: "draft" };

export function AdminCmsClient({ initialPages }: { initialPages: CmsPage[] }) {
  const { t } = useTranslations();
  const [pages, setPages] = useState(initialPages);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<CmsPage | null>(null);
  const [form, setForm] = useState(emptyForm);

  const statusOptions = useMemo(
    () => [
      { value: "draft", label: t("admin.draft") },
      { value: "published", label: t("admin.published") },
      { value: "archived", label: t("admin.archived") },
    ],
    [t]
  );

  const openNew = () => {
    setEditing(null);
    setForm(emptyForm);
    setShowForm(true);
  };

  const openEdit = (page: CmsPage) => {
    setEditing(page);
    setForm({ title: page.title, slug: page.slug, content: page.content, status: page.status });
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
    setEditing(null);
    setForm(emptyForm);
  };

  const handleSave = () => {
    if (editing) {
      setPages((prev) =>
        prev.map((p) =>
          p.id === editing.id
            ? { ...p, ...form, status: form.status as CmsPage["status"], updated_at: new Date().toISOString() }
            : p
        )
      );
    } else {
      const newPage: CmsPage = {
        id: `page-${Date.now()}`,
        title: form.title,
        slug: form.slug,
        content: form.content,
        meta_description: null,
        status: form.status as CmsPage["status"],
        sort_order: pages.length + 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        published_at: form.status === "published" ? new Date().toISOString() : null,
      };
      setPages((prev) => [...prev, newPage]);
    }
    closeForm();
  };

  const statusLabel = (status: string) => {
    if (status === "draft") return t("admin.draft");
    if (status === "published") return t("admin.published");
    if (status === "archived") return t("admin.archived");
    return status;
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.cmsTitle")}</h1>
          <p className="text-lg text-muted-foreground">{t("admin.cmsDesc")}</p>
        </div>
        <Button onClick={openNew}>
          <Plus className="h-5 w-5" aria-hidden="true" />
          {t("admin.newPage")}
        </Button>
      </header>

      {showForm && (
        <Card className="mb-6">
          <h2 className="mb-4 text-lg font-bold">{editing ? t("common.edit") : t("admin.newPage")}</h2>
          <div className="space-y-4">
            <Input label={t("admin.pageTitle")} value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            <Input label={t("admin.slugLabel")} value={form.slug} onChange={(e) => setForm({ ...form, slug: e.target.value })} />
            <div>
              <label htmlFor="content" className="mb-2 block font-semibold">{t("admin.content")}</label>
              <textarea
                id="content"
                value={form.content}
                onChange={(e) => setForm({ ...form, content: e.target.value })}
                rows={8}
                className="w-full rounded-xl border-2 border-border px-4 py-3 text-base focus:border-primary focus:outline-none"
              />
            </div>
            <Dropdown
              label={t("admin.status")}
              placeholder={t("admin.draft")}
              value={form.status}
              onChange={(value) => setForm({ ...form, status: value })}
              options={statusOptions}
              searchable={false}
            />
            <div className="flex gap-2">
              <Button onClick={handleSave}>{t("admin.savePage")}</Button>
              <Button variant="outline" onClick={closeForm}>{t("common.cancel")}</Button>
            </div>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {pages.map((page) => (
          <Card key={page.id} className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-bold">{page.title}</h2>
                <Badge variant={page.status === "published" ? "success" : "default"}>
                  {statusLabel(page.status)}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">/{page.slug}</p>
            </div>
            <Button variant="outline" size="sm" onClick={() => openEdit(page)}>
              <Pencil className="h-4 w-4" aria-hidden="true" />
              {t("common.edit")}
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
}
