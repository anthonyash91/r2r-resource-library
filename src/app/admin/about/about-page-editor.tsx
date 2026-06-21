"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import {
  ABOUT_SERVE_CARD_KEYS,
  ABOUT_VALUE_KEYS,
  type AboutContentFormValues,
} from "@/lib/about-content-fields";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

interface AboutPageEditorProps {
  initial: AboutContentFormValues;
}

export function AboutPageEditor({ initial }: AboutPageEditorProps) {
  const router = useRouter();
  const { t } = useTranslations();
  const [content, setContent] = useState(initial);
  const [saved, setSaved] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const updateField = (field: keyof AboutContentFormValues, value: string) => {
    setContent((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!isSupabaseConfigured()) {
      alert(t("admin.aboutSaveFailed"));
      return;
    }

    setSaving(true);
    setSaveMessage(null);

    try {
      const response = await fetch("/api/admin/about-content", {
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
        alert(data.error ?? t("admin.aboutSaveFailed"));
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
      alert(t("admin.aboutSaveFailed"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.aboutPageTitle")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.aboutPageDesc")}</p>
      </header>

      <div className="space-y-6">
        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.aboutHeroSection")}</h2>
          <Input
            label={t("admin.pageTitle")}
            value={content.about_hero_title}
            onChange={(e) => updateField("about_hero_title", e.target.value)}
          />
          <div>
            <label htmlFor="about-hero-description" className="mb-2 block font-semibold">
              {t("admin.metaDescription")}
            </label>
            <textarea
              id="about-hero-description"
              value={content.about_hero_description}
              onChange={(e) => updateField("about_hero_description", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.aboutMissionSection")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.about_mission_title}
            onChange={(e) => updateField("about_mission_title", e.target.value)}
          />
          <div>
            <label htmlFor="about-mission-p1" className="mb-2 block font-semibold">
              {t("admin.paragraphOne")}
            </label>
            <textarea
              id="about-mission-p1"
              value={content.about_mission_p1}
              onChange={(e) => updateField("about_mission_p1", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <div>
            <label htmlFor="about-mission-p2" className="mb-2 block font-semibold">
              {t("admin.paragraphTwo")}
            </label>
            <textarea
              id="about-mission-p2"
              value={content.about_mission_p2}
              onChange={(e) => updateField("about_mission_p2", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <div>
            <label htmlFor="about-mission-p3" className="mb-2 block font-semibold">
              {t("admin.paragraphThree")}
            </label>
            <textarea
              id="about-mission-p3"
              value={content.about_mission_p3}
              onChange={(e) => updateField("about_mission_p3", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.aboutServeSection")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.about_serve_title}
            onChange={(e) => updateField("about_serve_title", e.target.value)}
          />
          <div>
            <label htmlFor="about-serve-intro" className="mb-2 block font-semibold">
              {t("admin.sectionIntro")}
            </label>
            <textarea
              id="about-serve-intro"
              value={content.about_serve_intro}
              onChange={(e) => updateField("about_serve_intro", e.target.value)}
              rows={3}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <div className="space-y-3">
            <p className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
              {t("admin.audienceItems")}
            </p>
            {[1, 2, 3, 4, 5, 6].map((index) => {
              const field = `about_audience_${index}` as keyof AboutContentFormValues;
              return (
                <Input
                  key={field}
                  label={t("admin.audienceItem", { number: index })}
                  value={content[field]}
                  onChange={(e) => updateField(field, e.target.value)}
                />
              );
            })}
          </div>
          <div className="space-y-4">
            <p className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
              {t("admin.serviceCards")}
            </p>
            {ABOUT_SERVE_CARD_KEYS.map((key) => (
              <div key={key} className="rounded-xl border border-border p-4 space-y-3">
                <p className="font-semibold capitalize">{key}</p>
                <Input
                  label={t("admin.cardTitle")}
                  value={content[`about_serve_${key}_title` as keyof AboutContentFormValues]}
                  onChange={(e) =>
                    updateField(`about_serve_${key}_title` as keyof AboutContentFormValues, e.target.value)
                  }
                />
                <div>
                  <label className="mb-2 block font-semibold">{t("admin.cardDescription")}</label>
                  <textarea
                    value={content[`about_serve_${key}_desc` as keyof AboutContentFormValues]}
                    onChange={(e) =>
                      updateField(`about_serve_${key}_desc` as keyof AboutContentFormValues, e.target.value)
                    }
                    rows={2}
                    className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.aboutValuesSection")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.about_values_title}
            onChange={(e) => updateField("about_values_title", e.target.value)}
          />
          <div>
            <label htmlFor="about-values-subtitle" className="mb-2 block font-semibold">
              {t("admin.sectionIntro")}
            </label>
            <textarea
              id="about-values-subtitle"
              value={content.about_values_subtitle}
              onChange={(e) => updateField("about_values_subtitle", e.target.value)}
              rows={2}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          {ABOUT_VALUE_KEYS.map((key) => (
            <div key={key} className="rounded-xl border border-border p-4 space-y-3">
              <p className="font-semibold capitalize">{key}</p>
              <Input
                label={t("admin.cardTitle")}
                value={content[`about_values_${key}_title` as keyof AboutContentFormValues]}
                onChange={(e) =>
                  updateField(`about_values_${key}_title` as keyof AboutContentFormValues, e.target.value)
                }
              />
              <div>
                <label className="mb-2 block font-semibold">{t("admin.cardDescription")}</label>
                <textarea
                  value={content[`about_values_${key}_body` as keyof AboutContentFormValues]}
                  onChange={(e) =>
                    updateField(`about_values_${key}_body` as keyof AboutContentFormValues, e.target.value)
                  }
                  rows={3}
                  className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
                />
              </div>
            </div>
          ))}
        </Card>

        <Card className="space-y-4">
          <h2 className="text-xl font-bold">{t("admin.aboutCtaSection")}</h2>
          <Input
            label={t("admin.sectionHeading")}
            value={content.about_cta_title}
            onChange={(e) => updateField("about_cta_title", e.target.value)}
          />
          <div>
            <label htmlFor="about-cta-subtitle" className="mb-2 block font-semibold">
              {t("admin.sectionIntro")}
            </label>
            <textarea
              id="about-cta-subtitle"
              value={content.about_cta_subtitle}
              onChange={(e) => updateField("about_cta_subtitle", e.target.value)}
              rows={2}
              className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
            />
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <Input
              label={t("admin.primaryButtonLabel")}
              value={content.about_cta_browse}
              onChange={(e) => updateField("about_cta_browse", e.target.value)}
            />
            <Input
              label={t("admin.secondaryButtonLabel")}
              value={content.about_cta_contact}
              onChange={(e) => updateField("about_cta_contact", e.target.value)}
            />
          </div>
        </Card>

        <div className="space-y-2">
          <Button size="lg" onClick={handleSave} disabled={saving}>
            {saved
              ? t("admin.saved")
              : saving
                ? t("admin.savingAndTranslating")
                : t("admin.saveChanges")}
          </Button>
          {saveMessage ? (
            <p role="status" className="text-sm text-muted-foreground">
              {saveMessage}
            </p>
          ) : null}
        </div>
      </div>
    </div>
  );
}
