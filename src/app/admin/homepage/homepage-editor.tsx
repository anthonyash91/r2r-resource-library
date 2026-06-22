"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { FeaturedResourcesPicker } from "@/components/admin/featured-resources-picker";
import type { Resource } from "@/types";
import {
  EDITABLE_SITE_CONTENT_FIELDS,
  type SiteContentFormValues,
} from "@/lib/site-content-fields";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";
import { useConfirmDialog } from "@/components/ui/confirm-dialog";

interface HomepageEditorProps {
  initial: SiteContentFormValues;
  resources: Resource[];
}

function buildInitialContent(initial: SiteContentFormValues): SiteContentFormValues {
  return EDITABLE_SITE_CONTENT_FIELDS.reduce(
    (acc, field) => ({ ...acc, [field]: initial[field] ?? "" }),
    {} as SiteContentFormValues
  );
}

export function HomepageEditor({ initial, resources }: HomepageEditorProps) {
  const router = useRouter();
  const { t } = useTranslations();
  const { alert } = useConfirmDialog();
  const [content, setContent] = useState<SiteContentFormValues>(() => buildInitialContent(initial));
  const [saved, setSaved] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const updateField = (field: keyof SiteContentFormValues, value: string) => {
    setContent((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!isSupabaseConfigured()) {
      await alert({ title: t("common.error"), message: t("admin.homepageSaveFailed") });
      return;
    }

    setSaving(true);
    setSaveMessage(null);

    try {
      const response = await fetch("/api/admin/homepage-content", {
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
        await alert({
          title: t("common.error"),
          message: data.error ?? t("admin.homepageSaveFailed"),
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
      await alert({ title: t("common.error"), message: t("admin.homepageSaveFailed") });
    } finally {
      setSaving(false);
    }
  };

  const highlightMismatch =
    content.hero_headline_highlight.trim().length > 0 &&
    !content.hero_headline.includes(content.hero_headline_highlight);

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.homepageContent")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.homepageContentDesc")}</p>
      </header>

      <Card className="mb-8 space-y-6">
        <div>
          <h2 className="text-xl font-bold">{t("admin.siteBrandingSection")}</h2>
          <p className="mt-1 text-sm text-muted-foreground">{t("admin.siteBrandingSectionDesc")}</p>
        </div>

        <Input
          label={t("admin.navBrandName")}
          value={content.nav_brand_name}
          onChange={(e) => updateField("nav_brand_name", e.target.value)}
          hint={t("admin.navBrandNameHint")}
        />
        <Input
          label={t("admin.navTagline")}
          value={content.nav_tagline}
          onChange={(e) => updateField("nav_tagline", e.target.value)}
          hint={t("admin.navTaglineHint")}
        />
        <Input
          label={t("admin.footerTagline")}
          value={content.footer_tagline}
          onChange={(e) => updateField("footer_tagline", e.target.value)}
          hint={t("admin.footerTaglineHint")}
        />
        <div>
          <label htmlFor="footer-description" className="mb-2 block font-semibold">
            {t("admin.footerDescription")}
          </label>
          <textarea
            id="footer-description"
            value={content.footer_description}
            onChange={(e) => updateField("footer_description", e.target.value)}
            rows={3}
            className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
          />
          <p className="mt-1 text-sm text-muted-foreground">{t("admin.footerDescriptionHint")}</p>
        </div>
      </Card>

      <Card className="space-y-6">
        <div>
          <h2 className="text-xl font-bold">{t("admin.heroSection")}</h2>
          <p className="mt-1 text-sm text-muted-foreground">{t("admin.heroSectionDesc")}</p>
        </div>

        <Input
          label={t("admin.heroHeadline")}
          value={content.hero_headline}
          onChange={(e) => updateField("hero_headline", e.target.value)}
          hint={t("admin.homepageEnglishHint")}
        />
        <Input
          label={t("admin.heroHeadlineHighlight")}
          value={content.hero_headline_highlight}
          onChange={(e) => updateField("hero_headline_highlight", e.target.value)}
          hint={t("admin.heroHeadlineHighlightHint")}
          error={highlightMismatch ? t("admin.heroHeadlineHighlightMismatch") : undefined}
        />
        <div>
          <label htmlFor="subheadline" className="mb-2 block font-semibold">
            {t("admin.heroSubheadline")}
          </label>
          <textarea
            id="subheadline"
            value={content.hero_subheadline}
            onChange={(e) => updateField("hero_subheadline", e.target.value)}
            rows={3}
            className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
          />
        </div>
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
      </Card>

      <div className="mt-8">
        <FeaturedResourcesPicker resources={resources} />
      </div>
    </div>
  );
}
