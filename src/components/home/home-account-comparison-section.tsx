import Link from "next/link";
import { Check } from "lucide-react";
import type { ReactNode } from "react";
import { getServerTranslator } from "@/i18n/server";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { homeLightSectionShellClass, homeSectionSubtitleLeftClass, homeSectionSubtitleCompactMaxWidthClass } from "@/components/home/home-section-divider";
import { cn } from "@/lib/utils";
import { ScrollReveal } from "@/components/ui/scroll-reveal";

function FeatureRow({
  included,
  children,
}: {
  included: boolean;
  children: ReactNode;
}) {
  return (
    <div className="flex items-start gap-2.5">
      {included ? (
        <Check className="mt-0.5 h-4 w-4 shrink-0 text-[#2E9C6E]" strokeWidth={2.6} aria-hidden="true" />
      ) : (
        <span className="mt-0.5 shrink-0 text-[15px] font-bold text-[#b9bccb]" aria-hidden="true">
          –
        </span>
      )}
      <span className={`text-sm leading-snug ${included ? "text-foreground" : "text-[#9aa0b4]"}`}>
        {children}
      </span>
    </div>
  );
}

export async function HomeAccountComparisonSection() {
  const { t } = await getServerTranslator();

  return (
    <section
      className={cn(homeLightSectionShellClass, "py-[77px]")}
      aria-labelledby="home-account-comparison-heading"
    >
      <div className="grid items-center gap-10 lg:grid-cols-[0.85fr_1.15fr] lg:gap-[50px]">
        <ScrollReveal variant="slide-right">
          <div>
            <h2
              id="home-account-comparison-heading"
              className="font-heading text-[32px] font-extrabold tracking-tight text-foreground sm:text-4xl"
            >
              {t("home.accountComparisonTitle")}
            </h2>
            <p className={cn(homeSectionSubtitleLeftClass, homeSectionSubtitleCompactMaxWidthClass)}>
              {t("home.accountComparisonSubtitle")}
            </p>
          </div>
        </ScrollReveal>

        <div className="grid gap-[18px] sm:grid-cols-2">
          <ScrollReveal variant="fade-up">
            <div className="rounded-2xl border border-[var(--line)] bg-white p-7">
              <div className="font-heading text-[13px] font-bold uppercase tracking-[0.1em] text-muted-foreground">
                {t("home.noAccountLabel")}
              </div>
              <div className="mt-3.5 font-heading text-[26px] font-extrabold leading-tight text-foreground">
                {t("home.browseFreely")}
              </div>
              <p className="mb-5 mt-1 text-sm text-muted-foreground">{t("home.browseFreelyDesc")}</p>
              <div className="mb-6 flex flex-col gap-3">
                <FeatureRow included>{t("home.featureSearchAll")}</FeatureRow>
                <FeatureRow included>{t("home.featureHoursEligibility")}</FeatureRow>
                <FeatureRow included>{t("home.featureDirections")}</FeatureRow>
                <FeatureRow included={false}>{t("home.featureSavingNA")}</FeatureRow>
                <FeatureRow included={false}>{t("home.featureChecklistNA")}</FeatureRow>
              </div>
              <Link
                href={buildResourcesPageHref()}
                className="flex min-h-[44px] w-full items-center justify-center rounded-[10px] border-[1.5px] border-primary font-heading text-[15px] font-bold text-[var(--accent-ink)] transition-colors hover:bg-[#EFEAFE]"
              >
                {t("home.startBrowsing")}
              </Link>
            </div>
          </ScrollReveal>

          <ScrollReveal variant="fade-up" delay={75}>
            <div className="relative rounded-2xl border-[1.5px] border-primary bg-[#F9F8FF] p-7">
              <div className="absolute -top-2.5 right-5 rounded-full bg-primary px-2.5 py-1.5 font-heading text-[11px] font-bold uppercase tracking-[0.08em] text-primary-foreground">
                {t("home.recommendedBadge")}
              </div>
              <div className="font-heading text-[13px] font-bold uppercase tracking-[0.1em] text-[var(--accent-ink)]">
                {t("home.freeAccountLabel")}
              </div>
              <div className="mt-3.5 font-heading text-[26px] font-extrabold leading-tight text-foreground">
                {t("home.freeForever")}
              </div>
              <p className="mb-5 mt-1 text-sm text-muted-foreground">{t("home.freeForeverDesc")}</p>
              <div className="mb-6 flex flex-col gap-3">
                <FeatureRow included>
                  <strong className="font-bold">{t("home.everythingInBrowsing")}</strong>
                </FeatureRow>
                <FeatureRow included>{t("home.featureSaveOrganize")}</FeatureRow>
                <FeatureRow included>{t("home.featureTrackPlan")}</FeatureRow>
                <FeatureRow included>{t("home.featurePersonalizedChecklist")}</FeatureRow>
                <FeatureRow included>{t("home.featureReminders")}</FeatureRow>
              </div>
              <Link
                href="/signup"
                className="flex min-h-[44px] w-full items-center justify-center rounded-[10px] bg-primary font-heading text-[15px] font-bold text-primary-foreground transition-colors hover:bg-primary-hover"
              >
                {t("home.createFreeAccountArrow")}
              </Link>
            </div>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
