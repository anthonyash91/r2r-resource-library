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
import { useConfirmDialog } from "@/components/ui/confirm-dialog";
import {
  dateInputToEndsAt,
  isAnnouncementActive,
  isExpirationDateInPast,
} from "@/lib/announcements";
import { formatDate } from "@/lib/utils";

const emptyForm = {
  title: "",
  content: "",
  is_pinned: false,
  expires_on: "",
};

export function AdminAnnouncementsClient({ initial }: { initial: Announcement[] }) {
  const router = useRouter();
  const { t, locale } = useTranslations();
  const { confirm, alert } = useConfirmDialog();
  const [items, setItems] = useState(initial);
  const [form, setForm] = useState(emptyForm);
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);

  const handleSave = async () => {
    if (!form.title.trim() || !form.content.trim()) return;

    if (form.expires_on && isExpirationDateInPast(form.expires_on)) {
      await alert({ title: t("common.notice"), message: t("admin.announcementExpirationPast") });
      return;
    }

    setSaving(true);

    const payload = {
      title: form.title.trim(),
      content: form.content.trim(),
      status: "published" as const,
      is_pinned: form.is_pinned,
      starts_at: new Date().toISOString(),
      ends_at: form.expires_on ? dateInputToEndsAt(form.expires_on) : null,
    };

    if (isSupabaseConfigured()) {
      const supabase = createClient();
      if (supabase) {
        const { data, error } = await supabase.from("announcements").insert(payload).select().single();

        if (error || !data) {
          await alert({ title: t("common.error"), message: t("admin.announcementSaveFailed") });
          setSaving(false);
          return;
        }

        setItems((prev) => [data as Announcement, ...prev]);
        setForm(emptyForm);
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
    setForm(emptyForm);
    setShowForm(false);
    setSaving(false);
  };

  const handleDelete = async (announcement: Announcement) => {
    const confirmed = await confirm({
      title: t("common.remove"),
      message: t("admin.deleteAnnouncementConfirm"),
      confirmLabel: t("common.remove"),
      destructive: true,
    });
    if (!confirmed) return;

    if (isSupabaseConfigured()) {
      setBusyId(announcement.id);
      const supabase = createClient();
      if (supabase) {
        const { error } = await supabase.from("announcements").delete().eq("id", announcement.id);

        setBusyId(null);

        if (error) {
          await alert({ title: t("common.error"), message: t("admin.announcementDeleteFailed") });
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
          <Input
            label={t("admin.pageTitle")}
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
          <div>
            <label htmlFor="ann-content" className="mb-2 block font-semibold">
              {t("admin.content")}
            </label>
            <textarea
              id="ann-content"
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              rows={4}
              className="w-full rounded-xl border-2 border-border px-4 py-3"
            />
          </div>
          <Input
            type="date"
            label={t("admin.announcementExpirationDate")}
            hint={t("admin.announcementExpirationHint")}
            value={form.expires_on}
            onChange={(e) => setForm({ ...form, expires_on: e.target.value })}
          />
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={form.is_pinned}
              onChange={(e) => setForm({ ...form, is_pinned: e.target.checked })}
              className="h-5 w-5"
            />
            {t("admin.pinHomepage")}
          </label>
          <div className="flex gap-2">
            <Button onClick={handleSave} loading={saving}>
              {saving ? t("admin.saving") : t("admin.publish")}
            </Button>
            <Button variant="outline" onClick={() => setShowForm(false)}>
              {t("common.cancel")}
            </Button>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {items.map((ann) => {
          const active = isAnnouncementActive(ann);
          const expirationLabel = ann.ends_at
            ? t("admin.announcementExpiresOn", { date: formatDate(ann.ends_at, locale) })
            : null;

          return (
            <Card key={ann.id} className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <div className="mb-2 flex flex-wrap gap-2">
                  <Badge variant={active ? "success" : "default"}>
                    {active ? t("admin.published") : t("admin.announcementExpired")}
                  </Badge>
                  {ann.is_pinned && active ? (
                    <Badge variant="warning">{t("admin.pinHomepage")}</Badge>
                  ) : null}
                </div>
                <h2 className="text-lg font-bold">{ann.title}</h2>
                <p className="text-muted-foreground">{ann.content}</p>
                {expirationLabel ? (
                  <p className="mt-2 text-sm text-muted-foreground">{expirationLabel}</p>
                ) : null}
              </div>
              <Button variant="ghost" size="sm" onClick={() => handleDelete(ann)} loading={busyId === ann.id}>
                <Trash2 className="h-4 w-4" aria-hidden="true" />
                {t("common.remove")}
              </Button>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
