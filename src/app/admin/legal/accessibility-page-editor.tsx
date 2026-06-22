"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import {
  ACCESSIBILITY_FEATURE_KEYS,
  ACCESSIBILITY_PRINCIPLE_KEYS,
  type AccessibilityContentFormValues,
} from "@/lib/legal-content-fields";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";
import { useConfirmDialog } from "@/components/ui/confirm-dialog";

interface AccessibilityPageEditorProps {
  initial: AccessibilityContentFormValues;
}

export function AccessibilityPageEditor({ initial }: AccessibilityPageEditorProps) {
  const router = useRouter();
  const { t } = useTranslations();
  const { alert } = useConfirmDialog();
  const [content, setContent] = useState(initial);
  const [saved, setSaved] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const updateField = (field: keyof AccessibilityContentFormValues, value: string) => {
    setContent((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!isSupabaseConfigured()) {
      await alert({ title: t("common.error"), message: t("admin.legalSaveFailed") });
      return;
    }

    setSaving(true);
    setSaveMessage(null);

    try {
      const response = await fetch("/api/admin/legal-content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ document: "accessibility", content }),
      });

      const data = (await response.json()) as {
        success?: boolean;
        translated?: boolean;
        error?: string;
      };

      if (!response.ok) {
        await alert({
          title: t("common.error"),
          message: data.error ?? t("admin.legalSaveFailed"),
        });
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
      await alert({ title: t("common.error"), message: t("admin.legalSaveFailed") });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.legalAccessibilityPageTitle")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.legalAccessibilityPageDesc")}</p>
      </header>

      <div className="space-y-6">
        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.legalDocumentHeader")}</h2>
          <Input
            label={t("admin.pageTitle")}
            value={content.legal_accessibility_title}
            onChange={(e) => updateField("legal_accessibility_title", e.target.value)}
          />
          <div>
            <label htmlFor="a11y-description" className="mb-2 block font-semibold">
              {t("admin.metaDescription")}
            </label>
            <textarea
              id="a11y-description"
              value={content.legal_accessibility_description}
              onChange={(e) => updateField("legal_accessibility_description", e.target.value)}
              rows={2}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <Input
            label={t("admin.legalLastUpdatedDate")}
            value={content.legal_accessibility_last_updated}
            onChange={(e) => updateField("legal_accessibility_last_updated", e.target.value)}
          />
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.legalAccessibilityCommitment")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.legal_accessibility_commitment_title}
            onChange={(e) => updateField("legal_accessibility_commitment_title", e.target.value)}
          />
          <div>
            <label htmlFor="a11y-p1" className="mb-2 block font-semibold">
              {t("admin.paragraphOne")}
            </label>
            <textarea
              id="a11y-p1"
              value={content.legal_accessibility_commitment_p1}
              onChange={(e) => updateField("legal_accessibility_commitment_p1", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <div>
            <label htmlFor="a11y-p2" className="mb-2 block font-semibold">
              {t("admin.paragraphTwo")}
            </label>
            <textarea
              id="a11y-p2"
              value={content.legal_accessibility_commitment_p2}
              onChange={(e) => updateField("legal_accessibility_commitment_p2", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.legalAccessibilityWcag")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.legal_accessibility_wcag_title}
            onChange={(e) => updateField("legal_accessibility_wcag_title", e.target.value)}
          />
          {ACCESSIBILITY_PRINCIPLE_KEYS.map((key) => (
            <div key={key} className="space-y-3 rounded-xl border border-border p-4">
              <h3 className="font-semibold capitalize">{key}</h3>
              <Input
                label={t("admin.cardTitle")}
                value={content[`legal_accessibility_principle_${key}_title`]}
                onChange={(e) =>
                  updateField(`legal_accessibility_principle_${key}_title`, e.target.value)
                }
              />
              <div>
                <label htmlFor={`a11y-principle-${key}`} className="mb-2 block font-semibold">
                  {t("admin.cardDescription")}
                </label>
                <textarea
                  id={`a11y-principle-${key}`}
                  value={content[`legal_accessibility_principle_${key}_body`]}
                  onChange={(e) =>
                    updateField(`legal_accessibility_principle_${key}_body`, e.target.value)
                  }
                  rows={2}
                  className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
                />
              </div>
            </div>
          ))}
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.legalAccessibilityFeatures")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.legal_accessibility_features_title}
            onChange={(e) => updateField("legal_accessibility_features_title", e.target.value)}
          />
          {ACCESSIBILITY_FEATURE_KEYS.map((key) => (
            <div key={key} className="space-y-3 rounded-xl border border-border p-4">
              <h3 className="font-semibold capitalize">{key}</h3>
              <Input
                label={t("admin.cardTitle")}
                value={content[`legal_accessibility_feature_${key}_title`]}
                onChange={(e) =>
                  updateField(`legal_accessibility_feature_${key}_title`, e.target.value)
                }
              />
              <div>
                <label htmlFor={`a11y-feature-${key}`} className="mb-2 block font-semibold">
                  {t("admin.cardDescription")}
                </label>
                <textarea
                  id={`a11y-feature-${key}`}
                  value={content[`legal_accessibility_feature_${key}_body`]}
                  onChange={(e) =>
                    updateField(`legal_accessibility_feature_${key}_body`, e.target.value)
                  }
                  rows={3}
                  className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
                />
              </div>
            </div>
          ))}
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.legalAccessibilityLimitations")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.legal_accessibility_limitations_title}
            onChange={(e) => updateField("legal_accessibility_limitations_title", e.target.value)}
          />
          <div>
            <label htmlFor="a11y-limitations" className="mb-2 block font-semibold">
              {t("admin.legalSectionBody")}
            </label>
            <textarea
              id="a11y-limitations"
              value={content.legal_accessibility_limitations_body}
              onChange={(e) => updateField("legal_accessibility_limitations_body", e.target.value)}
              rows={4}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.legalAccessibilityReport")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.legal_accessibility_report_title}
            onChange={(e) => updateField("legal_accessibility_report_title", e.target.value)}
          />
          <div>
            <label htmlFor="a11y-report" className="mb-2 block font-semibold">
              {t("admin.legalSectionBody")}
            </label>
            <textarea
              id="a11y-report"
              value={content.legal_accessibility_report_body}
              onChange={(e) => updateField("legal_accessibility_report_body", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
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
