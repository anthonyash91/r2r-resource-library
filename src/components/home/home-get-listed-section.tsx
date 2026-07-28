import Link from "next/link";
import { CircleCheck, MapPin, Plus } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";
import {
  homeLightSectionShellClass,
  homeSectionBeforeDarkBandClass,
  homeSectionSubtitleClass,
  homeSectionSubtitleMaxWidthClass,
} from "@/components/home/home-section-divider";
import { cn } from "@/lib/utils";
import { ScrollReveal } from "@/components/ui/scroll-reveal";

const FEATURES = [
  {
    icon: Plus,
    iconBg: "bg-[#EFEAFE]",
    iconColor: "text-[var(--accent-ink)]",
    titleKey: "home.getListedFreeTitle",
    descKey: "home.getListedFreeDesc",
  },
  {
    icon: CircleCheck,
    iconBg: "bg-[#E4F6EE]",
    iconColor: "text-[#22835D]",
    titleKey: "home.getListedVerifiedTitle",
    descKey: "home.getListedVerifiedDesc",
  },
  {
    icon: MapPin,
    iconBg: "bg-[#FFE7E0]",
    iconColor: "text-[#E0593F]",
    titleKey: "home.getListedNearbyTitle",
    descKey: "home.getListedNearbyDesc",
  },
] as const;

export async function HomeGetListedSection() {
  const { t } = await getServerTranslator();

  return (
    <section
      className={cn(homeLightSectionShellClass, homeSectionBeforeDarkBandClass, "text-center")}
      aria-labelledby="home-get-listed-heading"
    >
      <ScrollReveal variant="fade-up">
        <h2
          id="home-get-listed-heading"
          className="font-heading text-[32px] font-extrabold tracking-tight text-foreground sm:text-[38px]"
        >
          {t("home.getListedTitle")}
        </h2>
        <p className={cn(homeSectionSubtitleClass, homeSectionSubtitleMaxWidthClass)}>
          {t("home.getListedSubtitle")}
        </p>
      </ScrollReveal>

      <div className="home-split-grid">
        <ScrollReveal variant="zoom-in" className="home-split-visual">
          <div className="relative w-full max-w-[420px] px-1.5 py-2">
            <div className="rounded-[18px] border border-[var(--line)] bg-white p-6">
              <div className="mb-3.5 flex items-center justify-between gap-2">
                <span className="rounded-[14px] bg-[#EFEAFE] px-3 py-1.5 font-heading text-[11px] font-bold uppercase text-[#5A3FC7]">
                  {t("home.mockCategoryHousing")}
                </span>
                <span className="inline-flex items-center gap-1 rounded-[14px] bg-[#E4F6EE] px-3 py-1.5 font-heading text-[11px] font-bold text-[var(--success)]">
                  <CircleCheck className="h-3 w-3" strokeWidth={3.4} aria-hidden="true" />
                  {t("home.mockVerified")}
                </span>
              </div>
              <div className="font-heading text-[19px] font-bold text-foreground">
                {t("home.getListedMockName")}
              </div>
              <div className="mt-2 flex flex-wrap items-center gap-2.5 text-[13px] font-medium text-muted-foreground">
                <span>{t("home.getListedMockCity")}</span>
                <span className="h-[3px] w-[3px] rounded-full bg-[#C7C5D2]" aria-hidden="true" />
                <span className="font-semibold text-[var(--success)]">{t("home.mockOpenNow")}</span>
                <span className="h-[3px] w-[3px] rounded-full bg-[#C7C5D2]" aria-hidden="true" />
                <span>{t("home.getListedMockIntake")}</span>
              </div>
              <div className="my-4 h-px bg-[var(--line)]" />
              <div className="mb-4 flex flex-wrap gap-1.5">
                {[t("home.mockTagFairChance"), t("home.mockTagNoFee")].map((tag) => (
                  <span
                    key={tag}
                    className="rounded-[13px] border border-[var(--line)] px-2.5 py-1.5 font-heading text-[11px] font-semibold text-[#5b6075]"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <div className="flex gap-2.5">
                <div className="flex-1 rounded-[9px] bg-primary py-3 text-center font-heading text-[13px] font-bold text-primary-foreground">
                  {t("home.mockCallNow")}
                </div>
                <div className="flex-1 rounded-[9px] border-[1.5px] border-[var(--line)] py-3 text-center font-heading text-[13px] font-bold text-foreground">
                  {t("home.mockSave")}
                </div>
              </div>
            </div>
            <div className="absolute -right-2 -top-1.5 rotate-[4deg] rounded-[11px] bg-[var(--coral)] px-2.5 py-2 text-center font-heading text-[10px] font-bold leading-tight text-white">
              {t("home.getListedPreviewBadge")}
            </div>
          </div>
        </ScrollReveal>

        <div className="home-split-features">
          {FEATURES.map(({ icon: Icon, iconBg, iconColor, titleKey, descKey }, index) => (
            <ScrollReveal key={titleKey} variant="fade-up" delay={index * 75}>
              <div className="flex gap-4">
                <div
                  className={`flex h-[46px] w-[46px] shrink-0 items-center justify-center rounded-xl ${iconBg}`}
                >
                  <Icon className={`h-[22px] w-[22px] ${iconColor}`} strokeWidth={2} aria-hidden="true" />
                </div>
                <div>
                  <h3 className="font-heading text-lg font-bold leading-[1.2] text-foreground">
                    {t(titleKey)}
                  </h3>
                  <p className="mt-1.5 text-[15px] leading-[1.6] text-muted-foreground">
                    {t(descKey)}
                  </p>
                </div>
              </div>
            </ScrollReveal>
          ))}
          <ScrollReveal variant="fade-up" delay={225}>
            <div className="mt-1.5 flex flex-wrap gap-3.5">
              <Link
                href="/contact"
                className="inline-flex min-h-[44px] items-center rounded-[10px] bg-primary px-6 py-3.5 font-heading text-[15px] font-bold text-primary-foreground transition-colors hover:bg-primary-hover"
              >
                {t("home.getListedCta")}
              </Link>
              <Link
                href="/faq"
                className="inline-flex min-h-[44px] items-center rounded-[10px] border-[1.5px] border-foreground/20 px-6 py-3.5 font-heading text-[15px] font-bold text-foreground transition-colors hover:bg-[var(--soft)]"
              >
                {t("home.getListedHowVerification")}
              </Link>
            </div>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
