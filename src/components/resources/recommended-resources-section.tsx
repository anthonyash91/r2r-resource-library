import Link from "next/link";
import { ArrowRight, Star } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { getServerTranslator } from "@/i18n/server";
import { cn, pageSectionPadding, pageSectionHeadingClass, pageSectionSubtitleClass } from "@/lib/utils";
import { buildResourcesPageHref, RECOMMENDED_RESOURCES_ID } from "@/lib/resources-page";
import { RecommendedPreferencesSummary } from "@/components/resources/recommended-preferences-summary";
import { CollapsibleRecommendedResourcesSection } from "@/components/resources/collapsible-recommended-resources-section";

interface RecommendedResourcesSectionProps {
  resources: Resource[];
  county?: string | null;
  state?: string | null;
  priorityCategories?: string[];
  variant?: "home" | "resources";
}

export async function RecommendedResourcesSection({
  resources,
  county,
  state,
  priorityCategories = [],
  variant = "home",
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
      ? buildResourcesPageHref({ state, county })
      : buildResourcesPageHref();

  if (variant === "resources") {
    return (
      <CollapsibleRecommendedResourcesSection
        title={title}
        subtitle={t("home.recommendedSubtitle")}
        resources={resources}
        preferencesSummary={
          <RecommendedPreferencesSummary
            state={state ?? null}
            county={county ?? null}
            priorityCategories={priorityCategories}
            variant={variant}
          />
        }
      />
    );
  }

  return (
    <section
      id={RECOMMENDED_RESOURCES_ID}
      className={cn(
        "scroll-mt-[var(--site-header-height)]",
        variant === "home"
          ? "app-band-muted"
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

          <ResourceMasonry resources={resources} columns={3} layout="masonry" />

          {variant === "home" ? (
            <div className="text-center">
              <Link
                href={browseHref}
                className="inline-flex min-h-[48px] items-center gap-2 text-base font-semibold text-primary hover:text-primary-hover"
              >
                {t("dashboard.browseMyCounty")}
                <ArrowRight className="h-5 w-5" aria-hidden="true" />
              </Link>
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}
