"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { FeaturedResourcesPicker } from "@/components/admin/featured-resources-picker";
import type { Resource } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

interface HomepageEditorProps {
  initial: Record<string, string>;
  resources: Resource[];
}

export function HomepageEditor({ initial, resources }: HomepageEditorProps) {
  const { t } = useTranslations();
  const [content, setContent] = useState({
    hero_headline: initial.hero_headline ?? "",
    hero_subheadline: initial.hero_subheadline ?? "",
  });
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
    await new Promise((r) => setTimeout(r, 300));
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.homepageContent")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.homepageContentDesc")}</p>
      </header>

      <Card className="space-y-6">
        <Input
          label={t("admin.heroHeadline")}
          value={content.hero_headline}
          onChange={(e) => setContent({ ...content, hero_headline: e.target.value })}
        />
        <div>
          <label htmlFor="subheadline" className="mb-2 block font-semibold">
            {t("admin.heroSubheadline")}
          </label>
          <textarea
            id="subheadline"
            value={content.hero_subheadline}
            onChange={(e) => setContent({ ...content, hero_subheadline: e.target.value })}
            rows={3}
            className="w-full rounded-xl border-2 border-border px-4 py-3 text-base"
          />
        </div>
        <Button size="lg" onClick={handleSave}>
          {saved ? t("admin.saved") : t("admin.saveChanges")}
        </Button>
      </Card>

      <div className="mt-8">
        <FeaturedResourcesPicker resources={resources} />
      </div>
    </div>
  );
}
