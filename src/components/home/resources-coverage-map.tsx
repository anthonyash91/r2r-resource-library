"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useTranslations } from "@/i18n/locale-context";
import { buildResourcesPageHref } from "@/lib/resources-page";
import {
  resourceMapPinRadius,
  type ResourceMapPin,
  type ResourceMapStateSummary,
} from "@/lib/resource-map-pins";
import { US_MAP_VIEWBOX, US_STATE_MAP_PATHS } from "@/lib/us-map/state-paths.generated";
import { cn } from "@/lib/utils";

interface ResourcesCoverageMapProps {
  pins: ResourceMapPin[];
  stateSummaries: ResourceMapStateSummary[];
  activeStates: string[];
}

export function ResourcesCoverageMap({
  pins,
  stateSummaries,
  activeStates,
}: ResourcesCoverageMapProps) {
  const { t } = useTranslations();
  const [hoveredPinKey, setHoveredPinKey] = useState<string | null>(null);
  const [hoveredState, setHoveredState] = useState<string | null>(null);

  const activeStateSet = useMemo(() => new Set(activeStates), [activeStates]);

  const pinKey = (pin: ResourceMapPin) =>
    pin.county ? `${pin.state}|${pin.county}` : `${pin.state}|statewide`;

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)] lg:items-start">
      <div className="rounded-2xl border border-border bg-card p-3 shadow-sm sm:p-4">
        <svg
          viewBox={`0 0 ${US_MAP_VIEWBOX.width} ${US_MAP_VIEWBOX.height}`}
          role="img"
          aria-label={t("home.coverageMapAria", { count: String(pins.length) })}
          className="h-auto w-full"
        >
          <title>{t("home.coverageMapTitle")}</title>
          <desc>{t("home.coverageMapDesc")}</desc>

          {US_STATE_MAP_PATHS.map((state) => {
            const isActive = activeStateSet.has(state.name);
            const isHovered = hoveredState === state.name;

            return (
              <path
                key={state.name}
                d={state.path}
                className={cn(
                  "transition-colors duration-200",
                  isActive
                    ? isHovered
                      ? "fill-primary/25 stroke-primary"
                      : "fill-primary/15 stroke-primary/50"
                    : "fill-muted/50 stroke-border/80"
                )}
                strokeWidth={isActive ? 1.25 : 0.75}
                onMouseEnter={() => setHoveredState(state.name)}
                onMouseLeave={() => setHoveredState((current) => (current === state.name ? null : current))}
              />
            );
          })}

          {pins.map((pin) => {
            const key = pinKey(pin);
            const radius = resourceMapPinRadius(pin.resourceCount);
            const isHovered = hoveredPinKey === key;

            return (
              <g
                key={key}
                onMouseEnter={() => setHoveredPinKey(key)}
                onMouseLeave={() => setHoveredPinKey((current) => (current === key ? null : current))}
              >
                <circle
                  cx={pin.x}
                  cy={pin.y}
                  r={isHovered ? radius + 0.75 : radius}
                  className={cn(
                    "fill-primary transition-[r]",
                    isHovered ? "opacity-100" : "opacity-80"
                  )}
                />
                <title>
                  {pin.county
                    ? t("home.coverageMapPinCounty", {
                        county: pin.county,
                        state: pin.state,
                        count: String(pin.resourceCount),
                      })
                    : t("home.coverageMapPinState", {
                        state: pin.state,
                        count: String(pin.resourceCount),
                      })}
                </title>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="space-y-5">
        <p className="text-base leading-relaxed text-muted-foreground">
          {t("home.coverageMapLegend")}
        </p>

        <ul className="space-y-3">
          {stateSummaries.map(({ state, resourceCount, countyCount }) => (
            <li key={state}>
              <Link
                href={buildResourcesPageHref({ state }, "results")}
                className="flex items-center justify-between gap-4 rounded-xl border border-border bg-card px-4 py-3 transition-colors hover:border-primary/40 hover:bg-primary/5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
              >
                <span className="font-semibold text-foreground">{state}</span>
                <span className="text-right text-sm text-muted-foreground">
                  {countyCount > 0
                    ? t("home.coverageMapStateSummaryCounties", {
                        resources: String(resourceCount),
                        counties: String(countyCount),
                      })
                    : t("home.coverageMapStateSummaryStatewide", {
                        resources: String(resourceCount),
                      })}
                </span>
              </Link>
            </li>
          ))}
        </ul>

        <Link
          href={buildResourcesPageHref()}
          className="inline-flex min-h-11 items-center text-sm font-semibold text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring rounded"
        >
          {t("home.coverageMapBrowseAll")}
        </Link>
      </div>
    </div>
  );
}
