import Link from "next/link";
import { MapPin } from "lucide-react";
import type { MatchedPathwayStep } from "@/lib/pathways/types";
import type { UserPreferences } from "@/lib/user-preferences/types";
import { PathwayCrisisCallout } from "@/components/pathways/pathway-crisis-callout";
import { PathwayStepSection } from "@/components/pathways/pathway-step-section";
import { PageHeroBand } from "@/components/layout/page-hero-band";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { getServerTranslator } from "@/i18n/server";
import { getPathwayIntroKey } from "@/lib/states/registry";
import { cn, pageSectionPadding } from "@/lib/utils";
import { ListOrdered } from "lucide-react";

interface PathwayViewProps {
  slug: string;
  matchedSteps: MatchedPathwayStep[];
  preferences: UserPreferences | null;
}

export async function PathwayView({ slug, matchedSteps, preferences }: PathwayViewProps) {
  const { t } = await getServerTranslator();
  const hasCounty = Boolean(preferences?.county?.trim());
  const introKey = getPathwayIntroKey(preferences?.state);

  return (
    <div>
      <PageHeroBand
        icon={ListOrdered}
        title={t("pathways.firstWeek.title")}
        description={t(introKey)}
      />

      <div className={cn("app-band-alt", pageSectionPadding)}>
        <div className="mx-auto max-w-4xl space-y-8">
          <p className="text-base leading-relaxed text-muted-foreground">
            {t("pathways.disclaimer")}
          </p>

          {!hasCounty ? (
            <Card className="flex flex-col gap-4 border-warning/40 bg-warning/5 p-5 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-start gap-3">
                <MapPin className="mt-0.5 h-5 w-5 shrink-0 text-warning" aria-hidden="true" />
                <div>
                  <p className="font-semibold text-foreground">
                    {t("pathways.setCountyBannerTitle")}
                  </p>
                  <p className="mt-1 text-base text-muted-foreground">
                    {t("pathways.setCountyBannerDesc")}
                  </p>
                </div>
              </div>
              <Link href="/get-started?edit=1" className="shrink-0">
                <Button>{t("pathways.setCountyCta")}</Button>
              </Link>
            </Card>
          ) : null}

          <PathwayCrisisCallout />

          <div className="mt-10">
            {matchedSteps.map((matched, index) => (
              <PathwayStepSection
                key={`${slug}-${matched.step.id}`}
                matched={matched}
                stepNumber={index + 1}
                preferences={preferences}
                isFirst={index === 0}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
