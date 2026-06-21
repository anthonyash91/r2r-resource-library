"use client";

import { useMemo, useState } from "react";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dropdown } from "@/components/ui/dropdown";
import { Card } from "@/components/ui/card";
import type { Faq } from "@/types";
import {
  DEFAULT_FAQ_CATEGORY,
  faqCategoryLabel,
  faqCategoryOptions,
} from "@/lib/faq-categories";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

const emptyForm = { question: "", answer: "", category: DEFAULT_FAQ_CATEGORY };

export function AdminFaqsClient({ initial }: { initial: Faq[] }) {
  const { t } = useTranslations();
  const [faqs, setFaqs] = useState(initial);
  const [form, setForm] = useState(emptyForm);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Faq | null>(null);
  const [saving, setSaving] = useState(false);

  const categoryOptions = useMemo(() => faqCategoryOptions(t), [t]);

  const openNew = () => {
    setEditing(null);
    setForm(emptyForm);
    setShowForm(true);
  };

  const openEdit = (faq: Faq) => {
    setEditing(faq);
    setForm({
      question: faq.question,
      answer: faq.answer,
      category: faq.category ?? DEFAULT_FAQ_CATEGORY,
    });
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
    setEditing(null);
    setForm(emptyForm);
  };

  const handleSave = async () => {
    if (!form.question.trim() || !form.answer.trim()) return;

    setSaving(true);

    if (editing) {
      const updated: Faq = {
        ...editing,
        question: form.question.trim(),
        answer: form.answer.trim(),
        category: form.category,
        updated_at: new Date().toISOString(),
      };

      if (isSupabaseConfigured()) {
        const supabase = createClient();
        if (supabase) {
          const { error } = await supabase
            .from("faqs")
            .update({
              question: updated.question,
              answer: updated.answer,
              category: updated.category,
            })
            .eq("id", editing.id);

          if (error) {
            alert(t("admin.faqSaveFailed"));
            setSaving(false);
            return;
          }
        }
      }

      setFaqs((prev) => prev.map((faq) => (faq.id === editing.id ? updated : faq)));
    } else {
      const sortOrder = faqs.length + 1;
      const payload = {
        question: form.question.trim(),
        answer: form.answer.trim(),
        category: form.category,
        sort_order: sortOrder,
        is_active: true,
      };

      if (isSupabaseConfigured()) {
        const supabase = createClient();
        if (supabase) {
          const { data, error } = await supabase.from("faqs").insert(payload).select().single();

          if (error || !data) {
            alert(t("admin.faqSaveFailed"));
            setSaving(false);
            return;
          }

          setFaqs((prev) => [...prev, data as Faq]);
          closeForm();
          setSaving(false);
          return;
        }
      }

      const faq: Faq = {
        id: `faq-${Date.now()}`,
        ...payload,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setFaqs((prev) => [...prev, faq]);
    }

    closeForm();
    setSaving(false);
  };

  const handleDelete = async (faq: Faq) => {
    if (!confirm(t("admin.deleteFaqConfirm"))) return;

    if (isSupabaseConfigured()) {
      const supabase = createClient();
      if (supabase) {
        const { error } = await supabase.from("faqs").delete().eq("id", faq.id);

        if (error) {
          alert(t("admin.faqDeleteFailed"));
          return;
        }
      }
    }

    setFaqs((prev) => prev.filter((item) => item.id !== faq.id));
    if (editing?.id === faq.id) closeForm();
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.faqManagement")}</h1>
        </div>
        <Button onClick={openNew}>
          <Plus className="h-5 w-5" aria-hidden="true" />
          {t("admin.newFaq")}
        </Button>
      </header>

      {showForm && (
        <Card className="mb-6 space-y-4">
          <h2 className="text-lg font-bold">{editing ? t("admin.editFaq") : t("admin.newFaq")}</h2>
          <Input
            label={t("admin.question")}
            value={form.question}
            onChange={(e) => setForm({ ...form, question: e.target.value })}
          />
          <div>
            <label htmlFor="answer" className="mb-2 block font-semibold">
              {t("admin.answer")}
            </label>
            <textarea
              id="answer"
              value={form.answer}
              onChange={(e) => setForm({ ...form, answer: e.target.value })}
              rows={4}
              className="w-full rounded-xl border-2 border-border px-4 py-3"
            />
          </div>
          <Dropdown
            label={t("admin.faqCategory")}
            placeholder={t("faq.general")}
            value={form.category}
            onChange={(value) => setForm({ ...form, category: value })}
            options={categoryOptions}
            searchable={false}
          />
          <div className="flex gap-2">
            <Button onClick={handleSave} disabled={saving}>
              {t("common.save")}
            </Button>
            <Button variant="outline" onClick={closeForm}>
              {t("common.cancel")}
            </Button>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {faqs.map((faq) => (
          <Card key={faq.id} className="flex items-start justify-between gap-4">
            <div className="min-w-0 flex-1">
              <p className="text-sm text-muted-foreground">
                {faqCategoryLabel(t, faq.category ?? DEFAULT_FAQ_CATEGORY)}
              </p>
              <h2 className="text-lg font-bold">{faq.question}</h2>
              <p className="text-muted-foreground">{faq.answer}</p>
            </div>
            <div className="flex shrink-0 gap-2">
              <Button variant="outline" size="sm" onClick={() => openEdit(faq)}>
                <Pencil className="h-4 w-4" aria-hidden="true" />
                {t("common.edit")}
              </Button>
              <Button variant="ghost" size="sm" onClick={() => handleDelete(faq)}>
                <Trash2 className="h-4 w-4" aria-hidden="true" />
                {t("admin.deleteFaq")}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
