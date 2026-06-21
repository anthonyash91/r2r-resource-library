"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Category } from "@/types";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

interface AdminCategoriesClientProps {
  initialCategories: Category[];
}

function slugify(name: string): string {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-");
}

export function AdminCategoriesClient({ initialCategories }: AdminCategoriesClientProps) {
  const { t } = useTranslations();
  const router = useRouter();
  const [categories, setCategories] = useState(initialCategories);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState({ name: "", description: "", icon: "search" });
  const [showNew, setShowNew] = useState(false);
  const [saving, setSaving] = useState(false);

  const resetForm = () => {
    setForm({ name: "", description: "", icon: "search" });
    setEditing(null);
    setShowNew(false);
  };

  const handleSave = async () => {
    const name = form.name.trim();
    if (!name) return;

    setSaving(true);

    const payload = {
      name,
      description: form.description.trim() || null,
      icon: form.icon.trim() || null,
    };

    if (editing) {
      if (isSupabaseConfigured()) {
        const supabase = createClient();
        if (supabase) {
          const { error } = await supabase
            .from("categories")
            .update(payload)
            .eq("id", editing);

          if (error) {
            alert(t("admin.categorySaveFailed"));
            setSaving(false);
            return;
          }
        }
      }

      setCategories((prev) =>
        prev.map((category) =>
          category.id === editing
            ? {
                ...category,
                ...payload,
                description: payload.description ?? "",
                icon: payload.icon ?? category.icon,
                updated_at: new Date().toISOString(),
              }
            : category
        )
      );
      resetForm();
      router.refresh();
      setSaving(false);
      return;
    }

    const insertPayload = {
      ...payload,
      slug: slugify(name),
      sort_order: categories.length + 1,
      is_active: true,
    };

    if (isSupabaseConfigured()) {
      const supabase = createClient();
      if (supabase) {
        const { data, error } = await supabase
          .from("categories")
          .insert(insertPayload)
          .select()
          .single();

        if (error || !data) {
          alert(t("admin.categorySaveFailed"));
          setSaving(false);
          return;
        }

        setCategories((prev) => [...prev, data as Category]);
        resetForm();
        router.refresh();
        setSaving(false);
        return;
      }
    }

    const newCategory: Category = {
      id: `cat-${Date.now()}`,
      name: insertPayload.name,
      slug: insertPayload.slug,
      description: insertPayload.description,
      icon: insertPayload.icon,
      sort_order: insertPayload.sort_order,
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    setCategories((prev) => [...prev, newCategory]);
    resetForm();
    setSaving(false);
  };

  const startEdit = (cat: Category) => {
    setEditing(cat.id);
    setForm({ name: cat.name, description: cat.description ?? "", icon: cat.icon ?? "search" });
    setShowNew(false);
  };

  const handleDelete = async (id: string) => {
    if (!confirm(t("admin.deleteCategoryConfirm"))) return;

    if (isSupabaseConfigured()) {
      const supabase = createClient();
      if (supabase) {
        const { error } = await supabase.from("categories").delete().eq("id", id);

        if (error) {
          alert(t("admin.categoryDeleteFailed"));
          return;
        }
      }
    }

    setCategories((prev) => prev.filter((category) => category.id !== id));
    if (editing === id) resetForm();
    router.refresh();
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.categoryManagement")}</h1>
          <p className="text-lg text-muted-foreground">{t("admin.categoryManagement")}</p>
        </div>
        <Button
          onClick={() => {
            setShowNew(true);
            setEditing(null);
            setForm({ name: "", description: "", icon: "search" });
          }}
        >
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
            <Input
              label={t("admin.categoryName")}
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
            <Input
              label={t("admin.description")}
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
            <Input
              label={t("admin.icon")}
              value={form.icon}
              onChange={(e) => setForm({ ...form, icon: e.target.value })}
            />
            <div className="flex gap-2">
              <Button onClick={handleSave} disabled={saving}>
                {t("common.save")}
              </Button>
              <Button variant="outline" onClick={resetForm}>
                {t("common.cancel")}
              </Button>
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
