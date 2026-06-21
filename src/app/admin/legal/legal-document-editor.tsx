"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { LEGAL_DOCUMENT_CONFIG, type LegalDocumentSlug } from "@/lib/legal-content-fields";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

interface LegalDocumentEditorProps {
  document: LegalDocumentSlug;
  initial: Record<string, string>;
}

export function LegalDocumentEditor({ document, initial }: LegalDocumentEditorProps) {
  const router = useRouter();
  const { t } = useTranslations();
  const [content, setContent] = useState(initial);
  const [saved, setSaved] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const config = LEGAL_DOCUMENT_CONFIG[document];
  const prefix = config.prefix;

  const titleKey =
    document === "privacy" ? "admin.legalPrivacyPageTitle" : "admin.legalTermsPageTitle";
  const descKey =
    document === "privacy" ? "admin.legalPrivacyPageDesc" : "admin.legalTermsPageDesc";

  const updateField = (field: string, value: string) => {
    setContent((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!isSupabaseConfigured()) {
      alert(t("admin.legalSaveFailed"));
      return;
    }

    setSaving(true);
    setSaveMessage(null);

    try {
      const response = await fetch("/api/admin/legal-content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ document, content }),
      });

      const data = (await response.json()) as {
        success?: boolean;
        translated?: boolean;
        error?: string;
      };

      if (!response.ok) {
        alert(data.error ?? t("admin.legalSaveFailed"));
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
      alert(t("admin.legalSaveFailed"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t(titleKey)}</h1>
        <p className="text-lg text-muted-foreground">{t(descKey)}</p>
      </header>

      <div className="space-y-6">
        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.legalDocumentHeader")}</h2>
          <Input
            label={t("admin.pageTitle")}
            value={content[`${prefix}_title`] ?? ""}
            onChange={(e) => updateField(`${prefix}_title`, e.target.value)}
          />
          <div>
            <label htmlFor="legal-description" className="mb-2 block font-semibold">
              {t("admin.metaDescription")}
            </label>
            <textarea
              id="legal-description"
              value={content[`${prefix}_description`] ?? ""}
              onChange={(e) => updateField(`${prefix}_description`, e.target.value)}
              rows={2}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <div>
            <label htmlFor="legal-intro" className="mb-2 block font-semibold">
              {t("admin.legalIntro")}
            </label>
            <textarea
              id="legal-intro"
              value={content[`${prefix}_intro`] ?? ""}
              onChange={(e) => updateField(`${prefix}_intro`, e.target.value)}
              rows={4}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <Input
            label={t("admin.legalLastUpdatedDate")}
            value={content[`${prefix}_last_updated`] ?? ""}
            onChange={(e) => updateField(`${prefix}_last_updated`, e.target.value)}
          />
          <Input
            label={t("admin.legalContactPrompt")}
            value={content[`${prefix}_contact_prompt`] ?? ""}
            onChange={(e) => updateField(`${prefix}_contact_prompt`, e.target.value)}
          />
        </Card>

        {config.sections.map((section) => (
          <Card key={section.id} className="space-y-4">
            <h2 className="text-xl font-bold">
              {t("admin.legalSectionLabel", { number: section.id.replace("s", "") })}
            </h2>
            <Input
              label={t("admin.sectionHeading")}
              value={content[`${prefix}_${section.id}_title`] ?? ""}
              onChange={(e) => updateField(`${prefix}_${section.id}_title`, e.target.value)}
            />
            {!section.contactLink ? (
              <div>
                <label htmlFor={`legal-${section.id}-body`} className="mb-2 block font-semibold">
                  {t("admin.legalSectionBody")}
                </label>
                <textarea
                  id={`legal-${section.id}-body`}
                  value={content[`${prefix}_${section.id}_body`] ?? ""}
                  onChange={(e) => updateField(`${prefix}_${section.id}_body`, e.target.value)}
                  rows={4}
                  className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
                />
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">{t("admin.legalContactSectionNote")}</p>
            )}
            {section.bullets?.map((bullet) => (
              <Input
                key={bullet}
                label={t("admin.legalBulletLabel", { number: bullet.replace("b", "") })}
                value={content[`${prefix}_${section.id}_bullet_${bullet}`] ?? ""}
                onChange={(e) =>
                  updateField(`${prefix}_${section.id}_bullet_${bullet}`, e.target.value)
                }
              />
            ))}
          </Card>
        ))}

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
