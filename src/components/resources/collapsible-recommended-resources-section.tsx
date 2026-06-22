"use client";

import { useEffect, useState, type ReactNode } from "react";
import { ChevronDown, Star } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { useTranslations } from "@/i18n/locale-context";
import { cn, blockInsetPadding, pageSectionSubtitleClass } from "@/lib/utils";
import { RECOMMENDED_RESOURCES_HASH, RECOMMENDED_RESOURCES_ID } from "@/lib/resources-page";

const STORAGE_KEY = "reentry_resources_recommended_open";

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
  const [open, setOpen] = useState(true);

  useEffect(() => {
    const forceOpen = window.location.hash === RECOMMENDED_RESOURCES_HASH;
    if (forceOpen) {
      setOpen(true);
      return;
    }

    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored === "0") setOpen(false);
    } catch {
      // ignore
    }
  }, []);

  const toggle = () => {
    setOpen((current) => {
      const next = !current;
      try {
        window.localStorage.setItem(STORAGE_KEY, next ? "1" : "0");
      } catch {
        // ignore
      }
      return next;
    });
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
        {open ? (
          <>
            <span className="min-w-0 flex-1">
              <span className="mb-2 flex items-center gap-2">
                <Star className="h-6 w-6 shrink-0 text-warning" aria-hidden="true" />
                <h2 id="recommended-resources-heading" className="m-0 text-2xl font-bold leading-6">
                  {title}
                </h2>
              </span>
              <span className={cn("block", pageSectionSubtitleClass)}>{subtitle}</span>
            </span>
            <ChevronDown
              className="mt-1 h-5 w-5 shrink-0 text-muted-foreground transition-transform rotate-180"
              aria-hidden="true"
            />
          </>
        ) : (
          <>
            <Star className="h-6 w-6 shrink-0 text-warning" aria-hidden="true" />
            <h2 id="recommended-resources-heading" className="m-0 min-w-0 flex-1 text-2xl font-bold leading-6">
              {title}
            </h2>
            <ChevronDown
              className="h-5 w-5 shrink-0 text-muted-foreground transition-transform"
              aria-hidden="true"
            />
          </>
        )}
        <span className="sr-only">
          {open ? t("resources.recommendedCollapseAria") : t("resources.recommendedExpandAria")}
        </span>
      </button>

      {open ? (
        <div
          id="recommended-resources-panel"
          className="rounded-b-xl border-t border-border px-4 pb-5 pt-4 sm:px-5"
        >
          {preferencesSummary}
          <ResourceMasonry resources={resources} columns={3} />
        </div>
      ) : null}
    </section>
  );
}
