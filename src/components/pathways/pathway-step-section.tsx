import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { MatchedPathwayStep } from "@/lib/pathways/types";
import type { UserPreferences } from "@/lib/user-preferences/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getServerTranslator } from "@/i18n/server";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { cn } from "@/lib/utils";

/** Extra room between pathway checklist steps. */
const pathwayStepDividerTop = "mt-14 border-t border-border pt-10";

interface PathwayStepSectionProps {
  matched: MatchedPathwayStep;
  stepNumber: number;
  preferences: UserPreferences | null;
  isFirst?: boolean;
}

export async function PathwayStepSection({
  matched,
  stepNumber,
  preferences,
  isFirst = false,
}: PathwayStepSectionProps) {
  const { t } = await getServerTranslator();
  const { step, resources, localResources, statewideResources, matchesUserPriority } =
    matched;

  const titleKey = `pathways.firstWeek.steps.${step.id}.title`;
  const descKey = `pathways.firstWeek.steps.${step.id}.description`;

  const browseSlug = step.browseCategorySlug ?? step.categorySlugs?.[0];
  const browseHref = buildResourcesPageHref(
    {
      ...(preferences?.state ? { state: preferences.state } : {}),
      ...(preferences?.county ? { county: preferences.county } : {}),
      ...(browseSlug ? { category: browseSlug } : {}),
    },
    "results"
  );

  const browseLabel =
    preferences?.county && preferences?.state
      ? t("pathways.browseCategoryInCounty", {
          category: t(`categories.${browseSlug}.shortName`),
          county: preferences.county,
        })
      : preferences?.state
        ? t("pathways.browseCategoryInState", {
            category: t(`categories.${browseSlug}.shortName`),
            state: preferences.state,
          })
        : t("pathways.browseCategory", {
            category: t(`categories.${browseSlug}.shortName`),
          });

  return (
    <section
      className={cn(!isFirst && pathwayStepDividerTop, isFirst && "mt-10")}
      aria-labelledby={`pathway-step-${step.id}-heading`}
    >
      <header className="mb-5 space-y-3">
        <div className="flex flex-wrap items-center gap-3">
          <span
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground"
            aria-hidden="true"
          >
            {stepNumber}
          </span>
          <h2
            id={`pathway-step-${step.id}-heading`}
            className="min-w-0 flex-1 text-xl font-bold sm:text-2xl"
          >
            {t(titleKey)}
          </h2>
          {matchesUserPriority ? (
            <Badge variant="primary" className="shrink-0">
              {t("pathways.matchesYourNeeds")}
            </Badge>
          ) : null}
        </div>
        <p className="text-base leading-relaxed text-muted-foreground">{t(descKey)}</p>
      </header>

      {resources.length > 0 ? (
        <div className="space-y-6">
          {localResources.length > 0 ? (
            <div>
              {statewideResources.length > 0 && preferences?.county ? (
                <h3 className="mb-3 text-base font-semibold text-foreground">
                  {t("pathways.localPrograms", { county: preferences.county })}
                </h3>
              ) : null}
              <ResourceMasonry resources={localResources} columns={2} layout="grid" contained />
            </div>
          ) : null}

          {statewideResources.length > 0 ? (
            <div>
              {localResources.length > 0 ? (
                <h3 className="mb-3 text-base font-semibold text-foreground">
                  {t("pathways.statewidePrograms", {
                    state: preferences?.state ?? t("pathways.yourState"),
                  })}
                </h3>
              ) : null}
              <ResourceMasonry
                resources={statewideResources}
                columns={2}
                layout="grid"
                contained
              />
            </div>
          ) : null}
        </div>
      ) : (
        <div className="rounded-xl border border-border bg-muted/40 p-5">
          <p className="text-base text-muted-foreground">
            {preferences?.county
              ? t("pathways.noLocalMatches", { county: preferences.county })
              : t("pathways.noMatches")}
          </p>
        </div>
      )}

      {browseSlug ? (
        <div className="mt-8 flex justify-center">
          <Link href={browseHref}>
            <Button variant="outline" size="sm" className="gap-2">
              {browseLabel}
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Button>
          </Link>
        </div>
      ) : null}
    </section>
  );
}
