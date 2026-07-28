"use client";

import Link from "next/link";
import {
  Briefcase,
  GraduationCap,
  Home as HomeIcon,
  ShieldCheck,
  Users,
} from "lucide-react";
import { homeSectionSubtitleMaxWidthClass } from "@/components/home/home-section-divider";
import { useTranslations } from "@/i18n/locale-context";
import { cn } from "@/lib/utils";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { ScrollReveal } from "@/components/ui/scroll-reveal";

const OUTCOME_CARDS = [
  {
    icon: HomeIcon,
    iconBg: "bg-[rgba(124,108,240,0.22)]",
    iconColor: "text-[#A99CF7]",
    titleKey: "home.possibleHousing",
    descKey: "home.possibleHousingDesc",
  },
  {
    icon: Briefcase,
    iconBg: "bg-[rgba(46,156,110,0.22)]",
    iconColor: "text-[#5FC79B]",
    titleKey: "home.possibleEmployment",
    descKey: "home.possibleEmploymentDesc",
  },
  {
    icon: Users,
    iconBg: "bg-[rgba(224,89,63,0.22)]",
    iconColor: "text-[#F0866B]",
    titleKey: "home.possibleFamily",
    descKey: "home.possibleFamilyDesc",
  },
  {
    icon: ShieldCheck,
    iconBg: "bg-[rgba(199,145,20,0.24)]",
    iconColor: "text-[#E0B34E]",
    titleKey: "home.possibleExpungement",
    descKey: "home.possibleExpungementDesc",
  },
  {
    icon: GraduationCap,
    iconBg: "bg-[rgba(194,78,120,0.24)]",
    iconColor: "text-[#DF85A6]",
    titleKey: "home.possibleEducation",
    descKey: "home.possibleEducationDesc",
  },
] as const;

export function HomePossibleStories() {
  const { t } = useTranslations();

  return (
    <div className="mx-auto max-w-[1180px] px-4 pt-[74px] text-center sm:px-9 sm:pt-[84px]">
      <ScrollReveal variant="fade-up">
        <h2
          id="home-possible-heading"
          className="font-heading text-[32px] font-extrabold tracking-tight text-white sm:text-[38px]"
        >
          {t("home.possibleTitle")}
        </h2>
        <p className={cn("mx-auto mt-4 text-[17px] leading-relaxed text-[#aab0c6]", homeSectionSubtitleMaxWidthClass)}>
          {t("home.possibleSubtitle")}
        </p>
      </ScrollReveal>

      <div className="mt-11 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {OUTCOME_CARDS.map(({ icon: Icon, iconBg, iconColor, titleKey, descKey }, index) => (
          <ScrollReveal key={titleKey} variant="fade-up" delay={index * 75}>
            <div className="rounded-2xl border border-white/10 bg-white/[0.025] px-4 py-6 text-center backdrop-blur-sm">
              <div
                className={`mx-auto mb-4 flex h-[54px] w-[54px] items-center justify-center rounded-[14px] ${iconBg}`}
              >
                <Icon className={`h-[26px] w-[26px] ${iconColor}`} strokeWidth={1.7} aria-hidden="true" />
              </div>
              <div className="font-heading text-[15px] font-bold leading-snug text-white">
                {t(titleKey)}
              </div>
              <p className="mt-2 text-[13px] leading-snug text-[#9aa1b8]">{t(descKey)}</p>
            </div>
          </ScrollReveal>
        ))}
      </div>

      <ScrollReveal variant="fade-up" delay={350}>
        <Link
          href={buildResourcesPageHref()}
          className="mt-9 inline-flex min-h-[44px] items-center rounded-[10px] bg-[#EFEAFE] px-7 py-3.5 font-heading text-[15px] font-bold text-[var(--accent-ink)] transition-opacity hover:opacity-90"
        >
          {t("home.exploreAllResources")}
        </Link>
      </ScrollReveal>
    </div>
  );
}
