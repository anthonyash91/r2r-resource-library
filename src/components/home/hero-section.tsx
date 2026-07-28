"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { MapPin, Search } from "lucide-react";
import { cn, resourcesHeroPadding } from "@/lib/utils";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { useSiteHeaderOffset } from "@/hooks/use-site-header-offset";
import { buildResourcesPageHref } from "@/lib/resources-page";
import {
  formatZipSearchDisplayValue,
  resourcesSearchParamsFromQuery,
} from "@/lib/resources-search-params";
import { useTranslations } from "@/i18n/locale-context";
import { ResourceFiltersPanel } from "@/components/resources/resource-filters-panel";
import type { ResourceFilterOptions } from "@/components/resources/use-resource-filter-options";
import { useResourceFilterDraftOptional } from "@/components/resources/resource-filter-draft-context";
import { HeroDecorativeShapes } from "@/components/home/hero-decorative-shapes";
import { HeroSurfaceOrbs } from "@/components/layout/hero-surface-orbs";

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
  const queryValue = preserveParams
    ? formatZipSearchDisplayValue(
        searchParams.get("zip") ?? undefined,
        searchParams.get("q") ?? undefined
      )
    : defaultValue;

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const query = (formData.get("q") as string) ?? "";
    const parsed = resourcesSearchParamsFromQuery(query);

    if (filterDraft) {
      filterDraft.apply({ q: query });
      return;
    }

    if (preserveParams) {
      const params = new URLSearchParams(searchParams.toString());
      params.delete("q");
      params.delete("zip");
      if (parsed.zip) params.set("zip", parsed.zip);
      if (parsed.q) params.set("q", parsed.q);
      router.push(buildResourcesPageHref(params, "results"), { scroll: false });
      return;
    }

    if (Object.keys(parsed).length > 0) {
      router.push(buildResourcesPageHref(parsed, "results"), { scroll: false });
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

interface HeroDualSearchBarProps {
  defaultNeed?: string;
  defaultZip?: string;
}

export function HeroDualSearchBar({ defaultNeed = "", defaultZip = "" }: HeroDualSearchBarProps) {
  const router = useRouter();
  const { t } = useTranslations();

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const need = ((formData.get("need") as string) ?? "").trim();
    const zip = ((formData.get("zip") as string) ?? "").trim();
    const params: { q?: string; zip?: string } = {};
    if (zip) params.zip = zip;
    if (need) params.q = need;
    router.push(
      Object.keys(params).length > 0
        ? buildResourcesPageHref(params, "results")
        : buildResourcesPageHref()
    );
  };

  return (
    <form
      onSubmit={handleSearch}
      role="search"
      aria-label={t("resources.searchAria")}
      className="mx-auto w-full max-w-[760px]"
    >
      <div className="flex flex-col gap-2 rounded-[15px] border border-[var(--line)] bg-white p-2 sm:flex-row sm:items-center sm:gap-1">
        <div className="flex min-w-0 flex-[1.5] items-center gap-2.5 px-3 py-3 sm:px-4">
          <Search className="h-[19px] w-[19px] shrink-0 text-muted-foreground" aria-hidden="true" />
          <input
            name="need"
            type="text"
            defaultValue={defaultNeed}
            placeholder={t("home.heroNeedPlaceholder")}
            aria-label={t("home.heroNeedPlaceholder")}
            className="hero-search-input min-h-[44px] w-full text-base text-foreground placeholder:text-muted-foreground"
          />
        </div>
        <div className="hidden h-7 w-px shrink-0 bg-[var(--line)] sm:block" aria-hidden="true" />
        <div className="flex min-w-0 flex-[0.85] items-center gap-2 px-3 py-3 sm:max-w-[148px] sm:px-4">
          <MapPin className="h-[17px] w-[17px] shrink-0 text-muted-foreground" aria-hidden="true" />
          <input
            name="zip"
            type="text"
            inputMode="numeric"
            pattern="[0-9]*"
            maxLength={5}
            defaultValue={defaultZip}
            placeholder={t("home.heroZipPlaceholder")}
            aria-label={t("home.heroZipPlaceholder")}
            className="hero-search-input min-h-[44px] w-full text-base text-foreground placeholder:text-muted-foreground"
          />
        </div>
        <button
          type="submit"
          className="inline-flex min-h-[52px] w-full shrink-0 cursor-pointer items-center justify-center rounded-[11px] bg-[var(--coral)] px-8 font-heading text-base font-bold text-white transition-opacity hover:opacity-90 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2 sm:w-auto"
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
      <span className="text-primary">{highlight}</span>
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
    { label: t("home.vettedResources", { count: resourceStat }), dot: "bg-primary" },
    { label: statesLabel, dot: "bg-[#FF9D6C]" },
    { label: t("home.freeAlways"), dot: "bg-[var(--coral)]" },
  ];

  return (
    <section className="home-hero-wash relative overflow-hidden px-4 pb-0 pt-16 text-center sm:px-9 sm:pt-[82px]">
      <HeroDecorativeShapes />

      <div className="relative mx-auto max-w-[1180px]">
        <ScrollReveal variant="fade-up">
          <h1 className="mx-auto max-w-[860px] font-heading text-4xl font-extrabold leading-[1.1] tracking-tight text-foreground sm:text-5xl lg:text-[56px]">
            {renderHeadline(headline, headlineHighlight)}
          </h1>
          <p className="mx-auto mt-4 max-w-[740px] font-sans text-[18px] font-normal leading-[1.65] text-muted-foreground">
            {subheadline}
          </p>
        </ScrollReveal>

        <ScrollReveal variant="fade-up" delay={75}>
          <div className="mt-8 flex flex-col gap-10">
            <HeroDualSearchBar />
            <div className="mb-2 flex flex-wrap items-center justify-center gap-1.5 sm:mb-3 sm:gap-2">
              <span className="text-[13px] font-medium leading-none text-muted-foreground">
                {t("home.popular")}
              </span>
              {popularTags.map(({ label, slug }) => (
                <Link
                  key={slug}
                  href={buildResourcesPageHref({ category: slug }, "results")}
                  className="rounded-full bg-[#EFEAFE] px-[14px] py-1.5 font-heading text-[13px] font-semibold leading-none text-[var(--accent-ink)] transition-opacity hover:opacity-80 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
                >
                  {label}
                </Link>
              ))}
            </div>
          </div>
        </ScrollReveal>

        <ScrollReveal variant="fade-up" delay={150}>
          <ul className="mt-6 flex flex-wrap items-center justify-center gap-x-6 gap-y-3 font-sans text-[14px] font-medium text-muted-foreground sm:mt-[24px]">
            {statItems.map(({ label, dot }) => (
              <li key={label} className="inline-flex items-center gap-1.5">
                <span className={cn("inline-block h-1.5 w-1.5 rounded-full", dot)} aria-hidden="true" />
                {label}
              </li>
            ))}
          </ul>
        </ScrollReveal>
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
