"use client";

import Link from "next/link";
import { Star } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Badge } from "@/components/ui/badge";
import { useTranslations } from "@/i18n/locale-context";
import { RECOMMENDED_RESOURCES_ID } from "@/lib/resources-page";

interface RecommendedResourcesSectionClientProps {
  resources: Resource[];
  county?: string | null;
}

export function RecommendedResourcesSectionClient({
  resources,
  county,
}: RecommendedResourcesSectionClientProps) {
  const { t } = useTranslations();

  if (resources.length === 0) return null;

  const title = county
    ? t("resources.recommendedPersonalized", { county })
    : t("dashboard.recommended");

  return (
    <section
      id={RECOMMENDED_RESOURCES_ID}
      className="scroll-mt-[var(--site-header-height)] w-full min-w-0"
      aria-labelledby="recommended-resources-heading"
    >
      <header className="mb-4 space-y-2">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex min-w-0 items-center gap-2">
            <Star className="h-5 w-5 shrink-0 text-warning" aria-hidden="true" />
            <h2 id="recommended-resources-heading" className="text-xl font-bold text-foreground">
              {title}
            </h2>
          </div>
          <Badge variant="primary" className="shrink-0 tabular-nums">
            {resources.length}
          </Badge>
        </div>
        <p className="text-base text-muted-foreground">
          {t("resources.recommendedPreferencesHintBefore")}{" "}
          <Link
            href="/dashboard"
            className="font-semibold text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
          >
            {t("resources.recommendedPreferencesHintLink")}
          </Link>
          {t("resources.recommendedPreferencesHintAfter")}
        </p>
      </header>
      <ResourceMasonry resources={resources} columns={3} layout="masonry" contained />
    </section>
  );
}
