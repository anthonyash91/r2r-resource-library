import Link from "next/link";
import { Check } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { HomeSectionRule } from "@/components/home/home-section-divider";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { CountUp } from "@/components/ui/count-up";
import { ReentryPlanProgressBar } from "@/components/home/reentry-plan-progress-bar";

const PLAN_ITEMS = [
  { key: "home.planItemId", done: true },
  { key: "home.planItemHousing", done: true },
  { key: "home.planItemHealth", done: true },
  { key: "home.planItemWork", inProgress: true },
  { key: "home.planItemBank", pending: true },
  { key: "home.planItemMentor", pending: true },
] as const;

export async function HomeHowItWorksSection() {
  const { t } = await getServerTranslator();

  const steps = [
    {
      num: "1",
      numBg: "bg-[#EFEAFE] text-[var(--accent-ink)]",
      cardBg: "bg-white",
      title: t("home.stepTellNeedTitle"),
      desc: t("home.stepTellNeedDesc"),
    },
    {
      num: "2",
      numBg: "bg-white text-[var(--coral)]",
      cardBg: "bg-[#FCE3EC] lg:translate-x-[18px]",
      title: t("home.stepVerifiedTitle"),
      desc: t("home.stepVerifiedDesc"),
    },
    {
      num: "3",
      numBg: "bg-[#E4F6EE] text-[#2E9C6E]",
      cardBg: "bg-white",
      title: t("home.stepNextTitle"),
      desc: t("home.stepNextDesc"),
    },
  ];

  return (
    <section
      id="how-it-works"
      className="app-dark-section scroll-mt-5 text-white"
      aria-labelledby="home-how-it-works-heading"
    >
      <div className="mx-auto max-w-[1180px] px-4 py-[79px] sm:px-9 sm:py-[93px]">
        <div className="grid items-center gap-10 lg:grid-cols-[1fr_1.1fr] lg:gap-[60px]">
          <ScrollReveal variant="slide-right">
            <div>
              <h2
                id="home-how-it-works-heading"
                className="font-heading text-[36px] font-extrabold leading-[1.15] tracking-[-0.02em] text-white"
              >
                {t("home.howItWorksTitle")}
              </h2>
              <p className="mt-5 font-sans text-[16px] font-normal leading-[1.7] text-[#aab0c6]">
                {t("home.howItWorksIntro1")}
              </p>
              <p className="mt-4 font-sans text-[16px] font-normal leading-[1.7] text-[#aab0c6]">
                {t("home.howItWorksIntro2")}
              </p>
              <Link
                href={buildResourcesPageHref()}
                className="mt-7 inline-flex min-h-[44px] items-center rounded-[10px] bg-primary px-6 py-3.5 font-heading text-[15px] font-bold text-primary-foreground transition-colors hover:bg-primary-hover"
              >
                {t("home.startSearching")}
              </Link>
            </div>
          </ScrollReveal>

          <div className="flex flex-col gap-3.5">
            {steps.map((step, index) => (
              <ScrollReveal key={step.num} variant="fade-up" delay={index * 75}>
                <div
                  className={`flex items-center gap-4 rounded-[14px] px-5 py-[18px] ${step.cardBg}`}
                >
                  <div
                    className={`flex h-[42px] w-[42px] shrink-0 items-center justify-center rounded-[11px] font-heading text-[16px] font-extrabold ${step.numBg}`}
                  >
                    {step.num}
                  </div>
                  <div>
                    <div className="font-heading text-[16px] font-bold leading-[1.2] text-foreground">
                      {step.title}
                    </div>
                    <div className="mt-[3px] font-sans text-[14px] font-normal leading-[1.5] text-muted-foreground">
                      {step.desc}
                    </div>
                  </div>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>

        <HomeSectionRule variant="dark" inset={false} />

        <div className="grid items-center gap-10 lg:grid-cols-[1fr_1.1fr] lg:gap-[60px]">
          <ScrollReveal variant="zoom-in" className="w-full">
            <div className="flex w-full justify-start">
              <div className="flex h-[302px] w-full flex-col rounded-[20px] bg-white p-7">
                <div className="mb-[9px] flex items-center justify-between gap-3">
                  <div className="font-heading text-[16px] font-bold leading-none text-foreground">
                    {t("home.reentryPlanTitle")}
                  </div>
                  <div className="font-heading text-[14px] font-bold leading-none text-primary">50%</div>
                </div>
                <div className="mb-3 h-[9px] overflow-hidden rounded-[5px] bg-[#ECEAF4]">
                  <ReentryPlanProgressBar />
                </div>
                <ul className="mt-0 flex flex-col gap-[9px]">
                  {PLAN_ITEMS.map((item) => (
                    <li key={item.key} className="flex items-center gap-[11px]">
                      {"done" in item && item.done ? (
                        <span className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full bg-[#2E9C6E]">
                          <Check
                            className="h-3 w-3 text-white"
                            strokeWidth={3.4}
                            aria-hidden="true"
                          />
                        </span>
                      ) : "inProgress" in item && item.inProgress ? (
                        <span
                          className="h-[22px] w-[22px] shrink-0 rounded-full border-[2.5px] border-[#FFB020]"
                          aria-hidden="true"
                        />
                      ) : (
                        <span
                          className="h-[22px] w-[22px] shrink-0 rounded-full border-[2.5px] border-[#D7D5E2]"
                          aria-hidden="true"
                        />
                      )}
                      <span
                        className={`font-heading text-[14px] font-semibold leading-none ${
                          "pending" in item && item.pending
                            ? "text-[#9A97AC]"
                            : "text-foreground"
                        }`}
                      >
                        {t(item.key)}
                        {"inProgress" in item && item.inProgress ? (
                          <>
                            {" — "}
                            <span className="text-[#E59400]">{t("home.planInProgress")}</span>
                          </>
                        ) : null}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </ScrollReveal>

          <ScrollReveal variant="fade-up" delay={75} className="w-full">
            <div className="w-full lg:pl-0">
              <h3 className="font-heading text-[32px] font-extrabold leading-[1.15] tracking-[-0.02em] text-white">
                {t("home.realOutcomesTitle")}
              </h3>
              <p className="mb-6 mt-4 font-sans text-[16px] font-normal leading-[1.7] text-[#aab0c6]">
                {t("home.realOutcomesDesc")}
              </p>
              <div className="flex gap-10">
                <div>
                  <div className="font-heading text-[38px] font-extrabold leading-none text-white">
                    <CountUp value="91%" />
                  </div>
                  <p className="mt-2 font-sans text-[14px] font-medium leading-[1.45] text-[#aab0c6]">
                    <span className="block">{t("home.statEmploymentLine1")}</span>
                    <span className="block">{t("home.statEmploymentLine2")}</span>
                  </p>
                </div>
                <div>
                  <div className="font-heading text-[38px] font-extrabold leading-none text-white">
                    <CountUp value="80%" />
                  </div>
                  <p className="mt-2 font-sans text-[14px] font-medium leading-[1.45] text-[#aab0c6]">
                    <span className="block">{t("home.statHomelessnessLine1")}</span>
                    <span className="block">{t("home.statHomelessnessLine2")}</span>
                  </p>
                </div>
              </div>
              <p className="mt-5 max-w-[430px] font-sans text-[12px] font-normal leading-[1.55] text-[#7e859b]">
                {t("home.realOutcomesSource")}{" "}
                <a
                  href="https://mn.gov/doc/assets/02-10MCORPPhase1EvaluationReport_tcm1089-272757.pdf"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[#aab0c6] underline underline-offset-2"
                >
                  {t("home.realOutcomesSourceLink")}
                </a>
                .
              </p>
            </div>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
