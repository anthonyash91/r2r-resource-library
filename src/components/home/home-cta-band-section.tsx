import Link from "next/link";
import { CircleCheck } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { homeLightSectionShellClass } from "@/components/home/home-section-divider";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { CountUp } from "@/components/ui/count-up";
import { cn } from "@/lib/utils";

interface HomeCtaBandSectionProps {
  resourceStat: string;
  stateCount: number;
  categoryCount: number;
}

export async function HomeCtaBandSection({
  resourceStat,
  stateCount,
  categoryCount,
}: HomeCtaBandSectionProps) {
  const { t } = await getServerTranslator();

  const features = [
    t("home.builtForFeature1"),
    t("home.builtForFeature2"),
    t("home.builtForFeature3"),
    t("home.builtForFeature4"),
  ];

  const statCards = [
    { value: resourceStat, label: t("home.statResources") },
    { value: String(stateCount), label: t("home.statStates") },
    { value: String(categoryCount), label: t("home.statCategories") },
    { value: "100%", label: t("home.statFree") },
  ];

  return (
    <section
      className={cn(homeLightSectionShellClass, "mb-[101px]")}
      aria-labelledby="home-cta-band-heading"
    >
      <div className="app-dark-section-card grid items-center gap-10 rounded-[22px] p-8 sm:p-12 lg:grid-cols-[1.05fr_0.95fr] lg:gap-[52px]">
        <ScrollReveal variant="slide-right">
          <div>
            <h2
              id="home-cta-band-heading"
              className="font-heading text-[30px] font-extrabold tracking-tight text-white sm:text-[34px]"
            >
              {t("home.builtForTitle")}
            </h2>
            <p className="mt-5 text-lg leading-relaxed text-[#c3c8da]">{t("home.builtForDesc")}</p>
            <ul className="mt-8 flex flex-col gap-4">
              {features.map((item) => (
                <li key={item} className="flex items-center gap-3">
                  <CircleCheck className="h-[22px] w-[22px] shrink-0 text-[#5fb98a]" aria-hidden="true" />
                  <span className="text-base font-medium text-[#e6e9f2]">{item}</span>
                </li>
              ))}
            </ul>
            <div className="mt-10 flex flex-wrap gap-3.5">
              <Link
                href="/signup"
                className="inline-flex min-h-[52px] items-center rounded-xl bg-white px-7 py-4 font-heading text-base font-bold text-[var(--accent-ink)] transition-opacity hover:opacity-90"
              >
                {t("home.createFreeAccountArrow")}
              </Link>
              <Link
                href={buildResourcesPageHref()}
                className="inline-flex min-h-[52px] items-center rounded-xl border-[1.5px] border-white/40 px-7 py-4 font-heading text-base font-bold text-white transition-colors hover:bg-white/10"
              >
                {t("home.browseResources")}
              </Link>
            </div>
          </div>
        </ScrollReveal>

        <div className="grid grid-cols-2 gap-4">
          {statCards.map(({ value, label }, index) => (
            <ScrollReveal key={label} variant="fade-up" delay={index * 75}>
              <div className="rounded-2xl border border-white/14 bg-white/[0.03] px-4 py-7 text-center backdrop-blur-sm sm:px-5 sm:py-8">
                <CountUp
                  value={value}
                  className="font-heading text-[34px] font-extrabold text-white"
                />
                <p className="mt-2 text-sm font-medium leading-snug text-[#aab0c6]">{label}</p>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
