"use client";

import { useSyncExternalStore, type ReactNode } from "react";
import { ChevronDown, Star } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { useTranslations } from "@/i18n/locale-context";
import { cn, blockInsetPadding, pageSectionSubtitleClass } from "@/lib/utils";
import { RECOMMENDED_RESOURCES_ID } from "@/lib/resources-page";
import {
  getRecommendedPanelOpen,
  setRecommendedPanelOpen,
  subscribeRecommendedPanelOpen,
} from "@/lib/resources-recommended-panel";

interface CollapsibleRecommendedResourcesSectionProps {
  title: string;
  subtitle: string;
  resources: Resource[];
  preferencesSummary: ReactNode;
}

export function CollapsibleRecommendedResourcesSection({
  title,
  subtitle,
  resources,
  preferencesSummary,
}: CollapsibleRecommendedResourcesSectionProps) {
  const { t } = useTranslations();
  const open = useSyncExternalStore(
    subscribeRecommendedPanelOpen,
    () => getRecommendedPanelOpen(window.location.hash),
    () => true
  );

  const toggle = () => {
    setRecommendedPanelOpen(!open);
  };

  return (
    <section
      id={RECOMMENDED_RESOURCES_ID}
      className="scroll-mt-[var(--site-header-height)] w-full min-w-0 rounded-xl border border-border bg-card"
      aria-labelledby="recommended-resources-heading"
    >
      <button
        type="button"
        className={cn(
          "flex w-full min-w-0 cursor-pointer gap-3 text-left focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
          blockInsetPadding,
          open ? "items-start rounded-t-xl" : "min-h-[52px] items-center rounded-xl"
        )}
        onClick={toggle}
        aria-expanded={open}
        aria-controls="recommended-resources-panel"
      >
        <span className="min-w-0 flex-1">
          <span className="flex items-center gap-2">
            <Star className="h-6 w-6 shrink-0 text-warning" aria-hidden="true" />
            <h2 id="recommended-resources-heading" className="m-0 min-w-0 flex-1 text-2xl font-bold leading-6">
              {title}
            </h2>
          </span>
          {open ? (
            <span className={cn("mt-2 block", pageSectionSubtitleClass)}>{subtitle}</span>
          ) : null}
        </span>
        <ChevronDown
          className={cn(
            "h-5 w-5 shrink-0 text-muted-foreground transition-transform",
            open ? "mt-0.5" : undefined,
            open && "rotate-180"
          )}
          aria-hidden="true"
        />
        <span className="sr-only">
          {open ? t("resources.recommendedCollapseAria") : t("resources.recommendedExpandAria")}
        </span>
      </button>

      {open ? (
        <div
          id="recommended-resources-panel"
          className={cn(
            "space-y-6 rounded-b-xl border-t border-border",
            blockInsetPadding
          )}
        >
          {preferencesSummary}
          <ResourceMasonry resources={resources} columns={3} layout="masonry" contained />
        </div>
      ) : null}
    </section>
  );
}
