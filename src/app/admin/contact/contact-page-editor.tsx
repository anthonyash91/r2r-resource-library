"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import type { ContactContentFormValues } from "@/lib/contact-content-fields";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

interface ContactPageEditorProps {
  initial: ContactContentFormValues;
}

export function ContactPageEditor({ initial }: ContactPageEditorProps) {
  const router = useRouter();
  const { t } = useTranslations();
  const [content, setContent] = useState(initial);
  const [saved, setSaved] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const updateField = (field: keyof ContactContentFormValues, value: string) => {
    setContent((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!isSupabaseConfigured()) {
      alert(t("admin.contactSaveFailed"));
      return;
    }

    setSaving(true);
    setSaveMessage(null);

    try {
      const response = await fetch("/api/admin/contact-content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(content),
      });

      const data = (await response.json()) as {
        success?: boolean;
        translated?: boolean;
        error?: string;
      };

      if (!response.ok) {
        alert(data.error ?? t("admin.contactSaveFailed"));
        setSaving(false);
        return;
      }

      setSaved(true);
      setSaveMessage(
        data.translated ? t("admin.homepageSavedWithTranslation") : t("admin.translationUnavailable")
      );
      router.refresh();
      setTimeout(() => {
        setSaved(false);
        setSaveMessage(null);
      }, 4000);
    } catch {
      alert(t("admin.contactSaveFailed"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.contactPageTitle")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.contactPageDesc")}</p>
      </header>

      <div className="space-y-6">
        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.contactHeroSection")}</h2>
          <Input
            label={t("admin.pageTitle")}
            value={content.contact_hero_title}
            onChange={(e) => updateField("contact_hero_title", e.target.value)}
          />
          <div>
            <label htmlFor="contact-hero-description" className="mb-2 block font-semibold">
              {t("admin.metaDescription")}
            </label>
            <textarea
              id="contact-hero-description"
              value={content.contact_hero_description}
              onChange={(e) => updateField("contact_hero_description", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.contactFormSection")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.contact_form_title}
            onChange={(e) => updateField("contact_form_title", e.target.value)}
          />
          <p className="text-sm text-muted-foreground">{t("admin.contactFormNote")}</p>
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.contactSidebarSection")}</h2>
          <Input
            label={t("admin.contactOtherWaysHeading")}
            value={content.contact_other_ways_title}
            onChange={(e) => updateField("contact_other_ways_title", e.target.value)}
          />
          <Input
            label={t("admin.contactResponseTimeHeading")}
            value={content.contact_response_time_title}
            onChange={(e) => updateField("contact_response_time_title", e.target.value)}
          />
          <div>
            <label htmlFor="contact-response-body" className="mb-2 block font-semibold">
              {t("admin.contactResponseTimeBody")}
            </label>
            <textarea
              id="contact-response-body"
              value={content.contact_response_time_body}
              onChange={(e) => updateField("contact_response_time_body", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
        </Card>

        <Card className="space-y-6">
          <h2 className="text-xl font-bold">{t("admin.contactHelpLinksSection")}</h2>
          <div className="space-y-4 rounded-xl border border-border p-4">
            <h3 className="font-semibold">{t("admin.contactHelpFaqs")}</h3>
            <Input
              label={t("admin.cardTitle")}
              value={content.contact_help_faqs_title}
              onChange={(e) => updateField("contact_help_faqs_title", e.target.value)}
            />
            <div>
              <label htmlFor="contact-faqs-desc" className="mb-2 block font-semibold">
                {t("admin.cardDescription")}
              </label>
              <textarea
                id="contact-faqs-desc"
                value={content.contact_help_faqs_desc}
                onChange={(e) => updateField("contact_help_faqs_desc", e.target.value)}
                rows={2}
                className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
              />
            </div>
          </div>
          <div className="space-y-4 rounded-xl border border-border p-4">
            <h3 className="font-semibold">{t("admin.contactHelpResources")}</h3>
            <Input
              label={t("admin.cardTitle")}
              value={content.contact_help_resources_title}
              onChange={(e) => updateField("contact_help_resources_title", e.target.value)}
            />
            <div>
              <label htmlFor="contact-resources-desc" className="mb-2 block font-semibold">
                {t("admin.cardDescription")}
              </label>
              <textarea
                id="contact-resources-desc"
                value={content.contact_help_resources_desc}
                onChange={(e) => updateField("contact_help_resources_desc", e.target.value)}
                rows={2}
                className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
              />
            </div>
          </div>
          <div className="space-y-4 rounded-xl border border-border p-4">
            <h3 className="font-semibold">{t("admin.contactHelpSuggest")}</h3>
            <Input
              label={t("admin.cardTitle")}
              value={content.contact_help_suggest_title}
              onChange={(e) => updateField("contact_help_suggest_title", e.target.value)}
            />
            <div>
              <label htmlFor="contact-suggest-desc" className="mb-2 block font-semibold">
                {t("admin.cardDescription")}
              </label>
              <textarea
                id="contact-suggest-desc"
                value={content.contact_help_suggest_desc}
                onChange={(e) => updateField("contact_help_suggest_desc", e.target.value)}
                rows={2}
                className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
              />
            </div>
          </div>
        </Card>

        <div className="flex flex-wrap items-center gap-4">
          <Button onClick={handleSave} disabled={saving}>
            {saving ? t("admin.saving") : t("admin.savePage")}
          </Button>
          {saved && saveMessage ? (
            <p className="text-sm text-muted-foreground">{saveMessage}</p>
          ) : null}
        </div>
      </div>
    </div>
  );
}
