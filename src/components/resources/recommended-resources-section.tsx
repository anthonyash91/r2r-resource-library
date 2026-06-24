import Link from "next/link";
import { ArrowRight, Star } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getServerTranslator } from "@/i18n/server";
import { cn, pageSectionPadding, pageSectionHeadingClass, pageSectionSubtitleClass, pageSectionBandClass, type PageSectionBand } from "@/lib/utils";
import { buildResourcesPageHref, RECOMMENDED_RESOURCES_ID } from "@/lib/resources-page";
import { RecommendedPreferencesSummary } from "@/components/resources/recommended-preferences-summary";

interface RecommendedResourcesSectionProps {
  resources: Resource[];
  county?: string | null;
  state?: string | null;
  priorityCategories?: string[];
  variant?: "home" | "resources";
  band?: PageSectionBand;
}

export async function RecommendedResourcesSection({
  resources,
  county,
  state,
  priorityCategories = [],
  variant = "home",
  band = "muted",
}: RecommendedResourcesSectionProps) {
  const { t } = await getServerTranslator();

  if (resources.length === 0) return null;

  const title =
    county && variant === "home"
      ? t("home.recommendedPersonalized", { county })
      : county && variant === "resources"
        ? t("resources.recommendedPersonalized", { county })
        : t("dashboard.recommended");

  const browseHref =
    state && county
      ? buildResourcesPageHref({ state, county }, "results")
      : buildResourcesPageHref();

  if (variant === "resources") {
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
              <h2
                id="recommended-resources-heading"
                className="text-xl font-bold text-foreground"
              >
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

  return (
    <section
      id={RECOMMENDED_RESOURCES_ID}
      className={cn(
        "scroll-mt-[var(--site-header-height)]",
        variant === "home"
          ? pageSectionBandClass(band)
          : "rounded-xl border border-border bg-card p-6",
        variant === "home" && pageSectionPadding
      )}
      aria-labelledby="recommended-resources-heading"
    >
      <div className={variant === "home" ? "mx-auto max-w-7xl" : undefined}>
        <header
          className={cn(
            variant === "home" ? "mb-8" : "mb-4",
            variant === "home" && "text-center"
          )}
        >
          <div
            className={cn(
              "mb-2 flex items-center gap-2",
              variant === "home" && "justify-center"
            )}
          >
            <Star className="h-6 w-6 text-warning" aria-hidden="true" />
            <h2
              id="recommended-resources-heading"
              className={variant === "home" ? pageSectionHeadingClass : "text-2xl font-bold"}
            >
              {title}
            </h2>
          </div>
          <p
            className={cn(
              pageSectionSubtitleClass,
              variant === "home" && "mx-auto max-w-2xl"
            )}
          >
            {t("home.recommendedSubtitle")}
          </p>
        </header>

        <div className="space-y-6">
          <RecommendedPreferencesSummary
            state={state ?? null}
            county={county ?? null}
            priorityCategories={priorityCategories}
            variant={variant}
          />

          <ResourceMasonry resources={resources} columns={3} layout="masonry" contained />
        </div>

        {variant === "home" ? (
          <div className="mt-10 flex justify-center">
              <Link href={browseHref} scroll={false}>
                <Button size="lg" variant="outline" className="gap-2">
                  {t("dashboard.browseMyCounty")}
                  <ArrowRight className="h-5 w-5" aria-hidden="true" />
                </Button>
              </Link>
            </div>
        ) : null}
      </div>
    </section>
  );
}
