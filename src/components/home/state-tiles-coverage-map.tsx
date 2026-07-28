"use client";

import Link from "next/link";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { cn } from "@/lib/utils";
import { buildCoverageTiles, type CoverageTile } from "@/lib/home/coverage-tiles";
import { homeSectionSubtitleCoverageMaxWidthClass } from "@/components/home/home-section-divider";
import { useTranslations } from "@/i18n/locale-context";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import type { Resource } from "@/types";

const STAGGER_MS = 75;

interface StateTilesCoverageMapProps {
  resources: Resource[];
  resourceStat: string;
  activeStateCount: number;
}

function CoverageTileCell({
  tile,
  index,
  visible,
}: {
  tile: CoverageTile;
  index: number;
  visible: boolean;
}) {
  return (
    <div
      className={cn(
        "scroll-reveal scroll-reveal--fade-up flex aspect-square items-center justify-center rounded-[10px] font-heading text-[11px] font-bold sm:text-[13px]",
        visible && "scroll-reveal--visible",
        tile.active
          ? "bg-primary text-primary-foreground shadow-[0_0_16px_rgba(124,108,240,0.6)]"
          : "bg-white/[0.05] text-white/[0.32]"
      )}
      style={
        {
          gridColumn: tile.col,
          gridRow: tile.row,
          "--scroll-reveal-delay": `${index * STAGGER_MS}ms`,
        } as CSSProperties
      }
    >
      {tile.abbr}
    </div>
  );
}

export function StateTilesCoverageMap({
  resources,
  resourceStat,
  activeStateCount,
}: StateTilesCoverageMapProps) {
  const { t } = useTranslations();
  const tiles = buildCoverageTiles(resources);
  const gridRef = useRef<HTMLDivElement>(null);
  const [gridVisible, setGridVisible] = useState(false);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setGridVisible(true);
      return;
    }

    const grid = gridRef.current;
    if (!grid) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setGridVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -7% 0px" }
    );

    observer.observe(grid);
    return () => observer.disconnect();
  }, []);

  return (
    <div className="grid gap-10 lg:grid-cols-2 lg:items-center lg:gap-16">
      <div
        ref={gridRef}
        className="mx-auto grid w-full max-w-[430px] grid-cols-8 gap-2.5"
        role="img"
        aria-label={t("home.coverageMapAria", { count: String(activeStateCount) })}
      >
        {tiles.map((tile, index) => (
          <CoverageTileCell key={tile.abbr} tile={tile} index={index} visible={gridVisible} />
        ))}
      </div>

      <ScrollReveal variant="slide-right">
        <div className="text-left">
          <p className="mb-4 font-heading text-[13px] font-bold uppercase tracking-[0.15em] text-[#9B8CF5]">
            {t("home.coverageEyebrow")}
          </p>
          <h2 className="font-heading text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            {t("home.coverageRootedTitle", { count: activeStateCount })}
          </h2>
          <p className={cn("mt-[18px] text-[17px] leading-relaxed text-[#aab0c6]", homeSectionSubtitleCoverageMaxWidthClass)}>
            {t("home.coverageRootedDesc", { count: resourceStat })}
          </p>
          <div className="mt-[30px] flex flex-col gap-3">
            <div className="flex items-center gap-3">
              <span className="h-[18px] w-[18px] shrink-0 rounded-[5px] bg-primary" aria-hidden="true" />
              <span className="text-[15px] font-medium text-[#cfd3e0]">
                {t("home.coverageLegendActive")}
              </span>
            </div>
            <div className="flex items-center gap-3">
              <span
                className="h-[18px] w-[18px] shrink-0 rounded-[5px] bg-white/[0.06]"
                aria-hidden="true"
              />
              <span className="text-[15px] font-medium text-[#8b93a8]">
                {t("home.coverageLegendExpanding")}
              </span>
            </div>
          </div>
          <Link
            href="/contact"
            className="mt-[30px] inline-block font-heading text-[15px] font-bold text-[#9B8CF5] transition-opacity hover:opacity-80"
          >
            {t("home.coverageGrowCta")}
          </Link>
        </div>
      </ScrollReveal>
    </div>
  );
}
