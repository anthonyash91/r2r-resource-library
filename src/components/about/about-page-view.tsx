import Link from "next/link";
import {
  ArrowRight,
  Briefcase,
  CircleCheck,
  Handshake,
  Heart,
  HeartPulse,
  Home,
  Scale,
  Shield,
  Users,
  Eye,
} from "lucide-react";
import { PageHeroBand } from "@/components/layout/page-hero-band";
import { HeroSurfaceOrbs } from "@/components/layout/hero-surface-orbs";
import { Card } from "@/components/ui/card";
import { cn, pageSectionPadding, checkIconClass, pageSectionSubtitleClass, pageSectionSubtitleOnHeroClass, pageSectionSubheadingClass } from "@/lib/utils";
import { buildResourcesPageHref } from "@/lib/resources-page";
import type { AboutPageContent } from "@/lib/about-content-fields";
import { getServerTranslator } from "@/i18n/server";

export interface AboutPageStats {
  resourceCount: string;
  stateCount: string;
  categoryCount: string;
  freeLabel: string;
}

interface AboutPageViewProps {
  content: AboutPageContent;
  stats: AboutPageStats;
}

const SERVE_ICONS = {
  housing: Home,
  employment: Briefcase,
  healthcare: HeartPulse,
  legal: Scale,
} as const;

const VALUE_ICONS = {
  dignity: Shield,
  accessibility: Eye,
  community: Users,
  trust: Handshake,
} as const;

const SERVE_CARD_KEYS = ["housing", "employment", "healthcare", "legal"] as const;
const VALUE_KEYS = ["dignity", "accessibility", "community", "trust"] as const;

export async function AboutPageView({ content, stats }: AboutPageViewProps) {
  const { t } = await getServerTranslator();

  const statCards = [
    { value: stats.resourceCount, label: t("home.statResources") },
    { value: stats.stateCount, label: t("home.statStates") },
    { value: stats.categoryCount, label: t("home.statCategories") },
    { value: stats.freeLabel, label: t("home.statFree") },
  ];

  return (
    <div>
      <PageHeroBand
        icon={Heart}
        title={content.heroTitle}
        description={content.heroDescription}
      />

      <section
        className={cn("bg-card", pageSectionPadding)}
        aria-labelledby="about-mission-heading"
      >
        <div className="mx-auto max-w-4xl text-center">
          <h2
            id="about-mission-heading"
            className="mb-6 text-3xl font-bold text-foreground sm:text-4xl"
          >
            {content.missionTitle}
          </h2>
          <p className="text-base leading-relaxed text-muted-foreground sm:text-lg">
            {content.missionP1}
          </p>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground sm:text-lg">
            {content.missionP2}
          </p>
          {content.missionP3.trim() ? (
            <p className="mt-4 text-base leading-relaxed text-muted-foreground sm:text-lg">
              {content.missionP3}
            </p>
          ) : null}

          <div className="mt-12 grid grid-cols-2 gap-4 sm:gap-5 lg:grid-cols-4">
            {statCards.map(({ value, label }) => (
              <div
                key={label}
                className="rounded-2xl border border-primary/10 bg-secondary px-4 py-8 text-center sm:px-5 sm:py-9"
              >
                <p className="text-3xl font-bold text-primary sm:text-4xl">{value}</p>
                <p className="mt-2 text-sm font-medium text-muted-foreground sm:text-base">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section
        className={cn("app-band-muted", pageSectionPadding)}
        aria-labelledby="about-serve-heading"
      >
        <div className="mx-auto grid max-w-6xl gap-10 lg:grid-cols-2 lg:items-center lg:gap-14">
          <div>
            <h2 id="about-serve-heading" className="mb-4 text-3xl font-bold text-foreground sm:text-4xl">
              {content.serveTitle}
            </h2>
            <p className={cn("mb-8 leading-relaxed", pageSectionSubtitleClass)}>
              {content.serveIntro}
            </p>
            <ul className="space-y-4">
              {content.audience.map((item) => (
                <li key={item} className="flex items-center gap-3">
                  <CircleCheck className={cn("h-5 w-5 shrink-0", checkIconClass)} aria-hidden="true" />
                  <span className="text-base leading-relaxed text-foreground">{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="space-y-4">
            {SERVE_CARD_KEYS.map((key) => {
              const Icon = SERVE_ICONS[key];
              const card = content.serveCards[key];
              return (
                <Card key={key} className="flex items-center gap-4 p-5 sm:p-6">
                  <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-secondary text-primary">
                    <Icon className="h-6 w-6" aria-hidden="true" />
                  </span>
                  <span>
                    <h3 className={pageSectionSubheadingClass}>{card.title}</h3>
                    <p className="mt-1 text-sm leading-relaxed text-muted-foreground sm:text-base">
                      {card.description}
                    </p>
                  </span>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      <section
        className={cn("bg-card", pageSectionPadding)}
        aria-labelledby="about-values-heading"
      >
        <div className="mx-auto max-w-6xl">
          <header className="mb-12 text-center">
            <h2 id="about-values-heading" className="text-3xl font-bold text-foreground sm:text-4xl">
              {content.valuesTitle}
            </h2>
            <p className={cn("mx-auto mt-3 max-w-2xl", pageSectionSubtitleClass)}>
              {content.valuesSubtitle}
            </p>
          </header>

          <div className="rounded-2xl bg-muted p-5 sm:p-8">
            <div className="grid gap-5 sm:grid-cols-2">
              {VALUE_KEYS.map((key) => {
                const Icon = VALUE_ICONS[key];
                const value = content.values[key];
                return (
                  <Card key={key} className="p-6 sm:p-7">
                    <span className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-secondary text-primary">
                      <Icon className="h-5 w-5" aria-hidden="true" />
                    </span>
                    <h3 className={cn("mb-2", pageSectionSubheadingClass)}>{value.title}</h3>
                    <p className="text-base leading-relaxed text-muted-foreground">{value.body}</p>
                  </Card>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      <section
        className={cn("app-hero-surface relative overflow-hidden", pageSectionPadding)}
        aria-labelledby="about-cta-heading"
      >
        <HeroSurfaceOrbs />
        <div className="relative mx-auto max-w-3xl text-center">
          <h2 id="about-cta-heading" className="text-3xl font-bold text-primary-foreground sm:text-4xl">
            {content.ctaTitle}
          </h2>
          <p className={cn("mx-auto mt-4 max-w-2xl", pageSectionSubtitleOnHeroClass)}>
            {content.ctaSubtitle}
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href={buildResourcesPageHref()}
              className={cn(
                "inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-xl bg-card px-8 py-3 text-lg font-semibold text-primary transition-colors",
                "hover:bg-card/90 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
              )}
            >
              {content.ctaBrowse}
              <ArrowRight className="h-5 w-5" aria-hidden="true" />
            </Link>
            <Link
              href="/contact"
              className={cn(
                "inline-flex min-h-[52px] cursor-pointer items-center gap-2 rounded-xl border-2 border-primary-foreground/40 bg-transparent px-8 py-3 text-lg font-semibold text-primary-foreground transition-colors",
                "hover:bg-primary-foreground/10 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
              )}
            >
              {content.ctaContact}
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
