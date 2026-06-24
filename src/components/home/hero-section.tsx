"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Search, CircleCheck } from "lucide-react";
import { cn, resourcesHeroPadding, checkIconClass } from "@/lib/utils";
import { HeroSurfaceOrbs } from "@/components/layout/hero-surface-orbs";
import { useSiteHeaderOffset } from "@/hooks/use-site-header-offset";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { useTranslations } from "@/i18n/locale-context";
import { ResourceFiltersPanel } from "@/components/resources/resource-filters-panel";
import type { ResourceFilterOptions } from "@/components/resources/use-resource-filter-options";
import { useResourceFilterDraftOptional } from "@/components/resources/resource-filter-draft-context";

interface HeroSearchBarProps {
  placeholder?: string;
  defaultValue?: string;
  compact?: boolean;
  sticky?: boolean;
  preserveParams?: boolean;
}

export function HeroSearchBar({
  placeholder,
  defaultValue = "",
  compact = false,
  sticky = false,
  preserveParams = false,
}: HeroSearchBarProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const filterDraft = useResourceFilterDraftOptional();
  const { t } = useTranslations();
  const searchPlaceholder = placeholder ?? t("home.heroSearchPlaceholder");
  const queryValue = preserveParams ? (searchParams.get("q") ?? "") : defaultValue;

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const query = (formData.get("q") as string) ?? "";

    if (filterDraft) {
      filterDraft.apply({ q: query });
      return;
    }

    if (preserveParams) {
      const params = new URLSearchParams(searchParams.toString());
      if (query?.trim()) {
        params.set("q", query.trim());
      } else {
        params.delete("q");
      }
      router.push(buildResourcesPageHref(params, "results"), { scroll: false });
      return;
    }

    if (query?.trim()) {
      router.push(buildResourcesPageHref({ q: query.trim() }, "results"), { scroll: false });
    } else {
      router.push(buildResourcesPageHref());
    }
  };

  return (
    <form
      onSubmit={handleSearch}
      role="search"
      aria-label={t("resources.searchAria")}
      className={cn("mx-auto w-full", sticky ? "max-w-2xl" : "max-w-3xl")}
    >
      <div
        className={cn(
          "flex items-center rounded-full bg-card",
          sticky
            ? "h-10 p-1 shadow-sm"
            : compact
              ? "h-12 p-1.5 shadow-md sm:h-14"
              : "h-16 p-1.5 shadow-lg"
        )}
      >
        <div className="relative min-w-0 flex-1 self-stretch">
          <Search
            className={cn(
              "pointer-events-none absolute top-1/2 -translate-y-1/2 text-muted-foreground",
              sticky
                ? "left-3 h-3.5 w-3.5"
                : compact
                  ? "left-3.5 h-4 w-4 sm:left-4 sm:h-5 sm:w-5"
                  : "left-4 h-5 w-5 sm:left-5"
            )}
            aria-hidden="true"
          />
          <input
            key={queryValue}
            name="q"
            type="text"
            inputMode="search"
            enterKeyHint="search"
            defaultValue={queryValue}
            placeholder={searchPlaceholder}
            aria-label={t("resources.searchAria")}
            className={cn(
              "hero-search-input h-full w-full bg-transparent text-foreground placeholder:text-muted-foreground",
              sticky
                ? "pl-9 pr-2 text-sm"
                : compact
                  ? "pl-10 pr-3 text-base sm:pl-12"
                  : "pl-11 pr-4 text-base sm:pl-14 sm:text-lg"
            )}
          />
        </div>
        <button
          type="submit"
          className={cn(
            "inline-flex h-full shrink-0 cursor-pointer items-center justify-center rounded-full bg-primary font-semibold text-primary-foreground transition-colors hover:bg-primary-hover focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
            sticky
              ? "px-4 text-sm"
              : compact
                ? "px-5 text-sm sm:px-8 sm:text-base"
                : "px-6 text-base sm:px-10 sm:text-lg"
          )}
        >
          {t("common.search")}
        </button>
      </div>
    </form>
  );
}

interface HeroSectionProps {
  headline: string;
  subheadline: string;
  highlight?: string;
  resourceStat: string;
  stateCount: number;
  popularTags: { label: string; slug: string }[];
}

function renderHeadline(headline: string, highlight: string) {
  const index = headline.indexOf(highlight);
  if (index === -1) {
    return headline;
  }

  const before = headline.slice(0, index);
  const after = headline.slice(index + highlight.length);

  return (
    <>
      {before}
      <span className="hero-headline-highlight">{highlight}</span>
      {after}
    </>
  );
}

export function HeroSection({
  headline,
  subheadline,
  highlight,
  resourceStat,
  stateCount,
  popularTags,
}: HeroSectionProps) {
  const { t } = useTranslations();
  const headlineHighlight = highlight ?? t("home.heroHighlight");

  const statesLabel =
    stateCount >= 50
      ? t("home.allStatesCovered")
      : t("home.stateCountCovered", { count: stateCount });

  const statItems = [
    t("home.vettedResources", { count: resourceStat }),
    statesLabel,
    t("home.freeAlways"),
  ];

  return (
    <section className="app-hero-surface relative flex min-h-[calc(100dvh-var(--site-header-height))] flex-col justify-center overflow-hidden px-4 py-16 sm:px-6 lg:px-8">
      <HeroSurfaceOrbs variant="home" />

      <div className="relative mx-auto w-full max-w-5xl text-center">
        <h1 className="mb-5 text-4xl font-bold leading-[1.08] text-primary-foreground sm:text-5xl sm:leading-[1.06] lg:text-6xl lg:leading-[1.05]">
          {renderHeadline(headline, headlineHighlight)}
        </h1>

        <p className="mx-auto mb-10 max-w-3xl text-lg leading-relaxed text-primary-foreground/90 sm:text-xl">
          {subheadline}
        </p>

        <HeroSearchBar />

        <div className="mt-10 flex flex-wrap items-center justify-center gap-2">
          <span className="text-sm font-medium text-primary-foreground/80 sm:text-base">
            {t("home.popular")}
          </span>
          {popularTags.map(({ label, slug }) => (
            <Link
              key={slug}
              href={buildResourcesPageHref({ category: slug }, "results")}
              className={cn(
                "rounded-full border border-primary-foreground/20 bg-primary-foreground/10 px-4 py-1.5 text-sm font-medium text-primary-foreground transition-colors",
                "hover:bg-primary-foreground/20 focus-visible:outline focus-visible:outline-3 focus-visible:outline-primary-foreground/60 focus-visible:outline-offset-2"
              )}
            >
              {label}
            </Link>
          ))}
        </div>

        <ul className="mt-6 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-sm text-primary-foreground/90 sm:text-base">
          {statItems.map((item) => (
            <li key={item} className="flex items-center gap-2">
              <CircleCheck
                className={cn("h-5 w-5 shrink-0", checkIconClass)}
                aria-hidden="true"
              />
              {item}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export function ResourcesHeroSection({
  states,
  globalOptions,
  appliedOptions,
}: {
  states: string[];
  globalOptions: ResourceFilterOptions;
  appliedOptions: ResourceFilterOptions;
}) {
  const { t } = useTranslations();
  const filterProps = { states, globalOptions, appliedOptions };
  const searchBarRef = useRef<HTMLDivElement | null>(null);
  const [showStickySearch, setShowStickySearch] = useState(false);
  const headerOffset = useSiteHeaderOffset();

  useEffect(() => {
    const node = searchBarRef.current;
    if (!node) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setShowStickySearch(!entry.isIntersecting);
      },
      {
        threshold: 0,
        rootMargin: `-${headerOffset}px 0px 0px 0px`,
      }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [headerOffset]);

  return (
    <>
      <div
        className={cn(
          "app-hero-surface fixed inset-x-0 z-50 overflow-hidden border-b border-primary-foreground/20 px-4 py-1.5 transition-[transform,opacity] duration-200 ease-out sm:px-6 sm:py-2 lg:px-8",
          showStickySearch
            ? "pointer-events-auto translate-y-0 opacity-100"
            : "pointer-events-none -translate-y-full opacity-0"
        )}
        style={{ top: headerOffset }}
      >
        <HeroSurfaceOrbs variant="sticky" />
        <div className="relative mx-auto w-full max-w-2xl">
          <HeroSearchBar sticky preserveParams placeholder={t("resources.searchPlaceholder")} />
        </div>
      </div>

      <section
        className={cn(
          "app-hero-surface relative z-10 px-4 sm:px-6 lg:px-8",
          resourcesHeroPadding
        )}
      >
        <HeroSurfaceOrbs />

        <div className="relative mx-auto w-full max-w-7xl">
          <div className="mx-auto flex w-full max-w-4xl flex-col items-center gap-4 text-center sm:gap-5">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold leading-none text-primary-foreground sm:text-4xl">
                {t("resources.findResources")}
              </h1>
              <p className="mx-auto max-w-2xl text-base leading-relaxed text-primary-foreground/90 sm:text-lg">
                {t("resources.heroSubheadline")}
              </p>
            </div>
            <div ref={searchBarRef} className="mx-auto w-full max-w-3xl space-y-4">
              <HeroSearchBar
                compact
                preserveParams
                placeholder={t("resources.searchPlaceholder")}
              />
              <ResourceFiltersPanel {...filterProps} />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
