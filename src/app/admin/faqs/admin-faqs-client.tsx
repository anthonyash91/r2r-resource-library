"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import type { Faq } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

export function AdminFaqsClient({ initial }: { initial: Faq[] }) {
  const { t } = useTranslations();
  const [faqs, setFaqs] = useState(initial);
  const [form, setForm] = useState({ question: "", answer: "", category: t("faq.general") });
  const [showForm, setShowForm] = useState(false);

  const handleSave = () => {
    const faq: Faq = {
      id: `faq-${Date.now()}`,
      question: form.question,
      answer: form.answer,
      category: form.category,
      sort_order: faqs.length + 1,
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    setFaqs((prev) => [...prev, faq]);
    setForm({ question: "", answer: "", category: t("faq.general") });
    setShowForm(false);
  };

  return (
    <div>
      <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">{t("admin.faqManagement")}</h1>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-5 w-5" aria-hidden="true" />
          {t("admin.newFaq")}
        </Button>
      </header>

      {showForm && (
        <Card className="mb-6 space-y-4">
          <Input label={t("admin.question")} value={form.question} onChange={(e) => setForm({ ...form, question: e.target.value })} />
          <div>
            <label htmlFor="answer" className="mb-2 block font-semibold">{t("admin.answer")}</label>
            <textarea id="answer" value={form.answer} onChange={(e) => setForm({ ...form, answer: e.target.value })} rows={4} className="w-full rounded-xl border-2 border-border px-4 py-3" />
          </div>
          <Input label={t("admin.faqCategory")} value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} />
          <div className="flex gap-2">
            <Button onClick={handleSave}>{t("common.save")}</Button>
            <Button variant="outline" onClick={() => setShowForm(false)}>{t("common.cancel")}</Button>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {faqs.map((faq) => (
          <Card key={faq.id}>
            <p className="text-sm text-muted-foreground">{faq.category}</p>
            <h2 className="text-lg font-bold">{faq.question}</h2>
            <p className="text-muted-foreground">{faq.answer}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
