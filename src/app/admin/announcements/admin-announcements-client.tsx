"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Announcement } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

export function AdminAnnouncementsClient({ initial }: { initial: Announcement[] }) {
  const { t } = useTranslations();
  const [items, setItems] = useState(initial);
  const [form, setForm] = useState({ title: "", content: "", is_pinned: false });
  const [showForm, setShowForm] = useState(false);

  const handleSave = () => {
    const ann: Announcement = {
      id: `ann-${Date.now()}`,
      title: form.title,
      content: form.content,
      status: "published",
      is_pinned: form.is_pinned,
      starts_at: new Date().toISOString(),
      ends_at: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    setItems((prev) => [ann, ...prev]);
    setForm({ title: "", content: "", is_pinned: false });
    setShowForm(false);
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
            <Button onClick={handleSave}>{t("admin.publish")}</Button>
            <Button variant="outline" onClick={() => setShowForm(false)}>{t("common.cancel")}</Button>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {items.map((ann) => (
          <Card key={ann.id}>
            <div className="mb-2 flex gap-2">
              <Badge variant="success">{t("admin.published")}</Badge>
              {ann.is_pinned && <Badge variant="warning">{t("admin.pinHomepage")}</Badge>}
            </div>
            <h2 className="text-lg font-bold">{ann.title}</h2>
            <p className="text-muted-foreground">{ann.content}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
