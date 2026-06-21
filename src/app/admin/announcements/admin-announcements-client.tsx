"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Announcement } from "@/types";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

export function AdminAnnouncementsClient({ initial }: { initial: Announcement[] }) {
  const router = useRouter();
  const { t } = useTranslations();
  const [items, setItems] = useState(initial);
  const [form, setForm] = useState({ title: "", content: "", is_pinned: false });
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    if (!form.title.trim() || !form.content.trim()) return;

    setSaving(true);

    const payload = {
      title: form.title.trim(),
      content: form.content.trim(),
      status: "published" as const,
      is_pinned: form.is_pinned,
      starts_at: new Date().toISOString(),
      ends_at: null,
    };

    if (isSupabaseConfigured()) {
      const supabase = createClient();
      if (supabase) {
        const { data, error } = await supabase.from("announcements").insert(payload).select().single();

        if (error || !data) {
          alert(t("admin.announcementSaveFailed"));
          setSaving(false);
          return;
        }

        setItems((prev) => [data as Announcement, ...prev]);
        setForm({ title: "", content: "", is_pinned: false });
        setShowForm(false);
        setSaving(false);
        router.refresh();
        return;
      }
    }

    const ann: Announcement = {
      id: `ann-${Date.now()}`,
      ...payload,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    setItems((prev) => [ann, ...prev]);
    setForm({ title: "", content: "", is_pinned: false });
    setShowForm(false);
    setSaving(false);
  };

  const handleDelete = async (announcement: Announcement) => {
    if (!confirm(t("admin.deleteAnnouncementConfirm"))) return;

    if (isSupabaseConfigured()) {
      const supabase = createClient();
      if (supabase) {
        const { error } = await supabase.from("announcements").delete().eq("id", announcement.id);

        if (error) {
          alert(t("admin.announcementDeleteFailed"));
          return;
        }
        router.refresh();
      }
    }

    setItems((prev) => prev.filter((item) => item.id !== announcement.id));
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.announcementsTitle")}</h1>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-5 w-5" aria-hidden="true" />
          {t("admin.newAnnouncement")}
        </Button>
      </header>

      {showForm && (
        <Card className="mb-6 space-y-4">
          <Input label={t("admin.pageTitle")} value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          <div>
            <label htmlFor="ann-content" className="mb-2 block font-semibold">{t("admin.content")}</label>
            <textarea
              id="ann-content"
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              rows={4}
              className="w-full rounded-xl border-2 border-border px-4 py-3"
            />
          </div>
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={form.is_pinned} onChange={(e) => setForm({ ...form, is_pinned: e.target.checked })} className="h-5 w-5" />
            {t("admin.pinHomepage")}
          </label>
          <div className="flex gap-2">
            <Button onClick={handleSave} disabled={saving}>
              {saving ? t("admin.saving") : t("admin.publish")}
            </Button>
            <Button variant="outline" onClick={() => setShowForm(false)}>{t("common.cancel")}</Button>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {items.map((ann) => (
          <Card key={ann.id} className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <div className="mb-2 flex gap-2">
                <Badge variant="success">{t("admin.published")}</Badge>
                {ann.is_pinned && <Badge variant="warning">{t("admin.pinHomepage")}</Badge>}
              </div>
              <h2 className="text-lg font-bold">{ann.title}</h2>
              <p className="text-muted-foreground">{ann.content}</p>
            </div>
            <Button variant="ghost" size="sm" onClick={() => handleDelete(ann)}>
              <Trash2 className="h-4 w-4" aria-hidden="true" />
              {t("common.remove")}
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
}
