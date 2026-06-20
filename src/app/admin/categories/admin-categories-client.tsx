"use client";

import { useState } from "react";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Category } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

interface AdminCategoriesClientProps {
  initialCategories: Category[];
}

export function AdminCategoriesClient({ initialCategories }: AdminCategoriesClientProps) {
  const { t } = useTranslations();
  const [categories, setCategories] = useState(initialCategories);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState({ name: "", description: "", icon: "search" });
  const [showNew, setShowNew] = useState(false);

  const handleSave = () => {
    if (editing) {
      setCategories((prev) =>
        prev.map((c) =>
          c.id === editing
            ? { ...c, name: form.name, description: form.description, icon: form.icon }
            : c
        )
      );
      setEditing(null);
    } else {
      const newCat: Category = {
        id: `cat-${Date.now()}`,
        name: form.name,
        slug: form.name.toLowerCase().replace(/\s+/g, "-"),
        description: form.description,
        icon: form.icon,
        sort_order: categories.length + 1,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setCategories((prev) => [...prev, newCat]);
      setShowNew(false);
    }
    setForm({ name: "", description: "", icon: "search" });
  };

  const startEdit = (cat: Category) => {
    setEditing(cat.id);
    setForm({ name: cat.name, description: cat.description ?? "", icon: cat.icon ?? "search" });
    setShowNew(false);
  };

  const handleDelete = (id: string) => {
    if (!confirm(t("admin.deleteCategoryConfirm"))) return;
    setCategories((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.categoryManagement")}</h1>
          <p className="text-lg text-muted-foreground">{t("admin.categoryManagement")}</p>
        </div>
        <Button onClick={() => { setShowNew(true); setEditing(null); setForm({ name: "", description: "", icon: "search" }); }}>
          <Plus className="h-5 w-5" aria-hidden="true" />
          {t("admin.newCategory")}
        </Button>
      </header>

      {(showNew || editing) && (
        <Card className="mb-6">
          <h2 className="mb-4 text-lg font-bold">
            {editing ? t("admin.editCategory") : t("admin.newCategory")}
          </h2>
          <div className="space-y-4">
            <Input label={t("admin.categoryName")} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <Input label={t("admin.description")} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            <Input label={t("admin.icon")} value={form.icon} onChange={(e) => setForm({ ...form, icon: e.target.value })} />
            <div className="flex gap-2">
              <Button onClick={handleSave}>{t("common.save")}</Button>
              <Button variant="outline" onClick={() => { setEditing(null); setShowNew(false); }}>{t("common.cancel")}</Button>
            </div>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {categories.map((cat) => (
          <Card key={cat.id} className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-bold">{cat.name}</h2>
                {!cat.is_active && <Badge>{t("admin.inactive")}</Badge>}
              </div>
              <p className="text-sm text-muted-foreground">{cat.description}</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={() => startEdit(cat)}>
                <Pencil className="h-4 w-4" aria-hidden="true" />
                {t("common.edit")}
              </Button>
              <Button variant="ghost" size="sm" onClick={() => handleDelete(cat.id)}>
                <Trash2 className="h-4 w-4" aria-hidden="true" />
                {t("admin.deleteCategory")}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
