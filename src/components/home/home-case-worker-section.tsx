import Link from "next/link";
import { Calendar, ClipboardList, Send } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";
import { homeLightSectionShellClass, homeSectionSubtitleClass, homeSectionSubtitleMaxWidthClass } from "@/components/home/home-section-divider";
import { cn } from "@/lib/utils";
import { ScrollReveal } from "@/components/ui/scroll-reveal";

const FEATURES = [
  {
    icon: ClipboardList,
    iconBg: "bg-[#EFEAFE]",
    iconColor: "text-[var(--accent-ink)]",
    titleKey: "home.caseWorkerFeature1Title",
    descKey: "home.caseWorkerFeature1Desc",
  },
  {
    icon: Send,
    iconBg: "bg-[#E4F6EE]",
    iconColor: "text-[#22835D]",
    titleKey: "home.caseWorkerFeature2Title",
    descKey: "home.caseWorkerFeature2Desc",
  },
  {
    icon: Calendar,
    iconBg: "bg-[#FFE7E0]",
    iconColor: "text-[#E0593F]",
    titleKey: "home.caseWorkerFeature3Title",
    descKey: "home.caseWorkerFeature3Desc",
  },
] as const;

function CaseWorkerMock() {
  return (
    <div className="mx-auto h-[268px] w-full max-w-[408px] overflow-hidden rounded-[18px] border border-[var(--line)] bg-white">
      <div className="flex h-full">
        <div className="flex w-[140px] shrink-0 flex-col gap-1.5 border-r border-[var(--line)] bg-[var(--soft)] p-3">
          <div className="mb-3 flex items-center gap-1.5">
            <div className="h-5 w-5 rounded-md bg-primary" />
            <div className="h-2 w-[54px] rounded bg-[#E4E2F0]" />
          </div>
          <div className="rounded-md bg-[#EFEAFE] px-2.5 py-2">
            <div className="h-1.5 w-[60px] rounded bg-primary" />
          </div>
          {[70, 50, 64].map((w) => (
            <div key={w} className="px-2.5 py-2">
              <div className="h-1.5 rounded bg-[#E4E2F0]" style={{ width: w }} />
            </div>
          ))}
        </div>
        <div className="flex-1 p-3.5">
          <div className="mb-4 h-2 w-[120px] rounded bg-[#E4E2F0]" />
          <div className="mb-4 grid grid-cols-3 gap-2.5">
            {["bg-primary", "bg-[#FFB35C]", "bg-[#2E9C6E]"].map((color) => (
              <div key={color} className="rounded-[10px] border border-[var(--line)] p-3">
                <div className={`mb-1.5 h-4 w-[30px] rounded ${color}`} />
                <div className="h-1.5 w-4/5 rounded bg-[#EFEEF6]" />
              </div>
            ))}
          </div>
          <div className="flex flex-col gap-2">
            {[
              { avatar: "bg-[#EFEAFE]", badge: "bg-[#E4F6EE]" },
              { avatar: "bg-[#FFE7E0]", badge: "bg-[#FFF3D6]" },
              { avatar: "bg-[#E4F6EE]", badge: "bg-[#E4F6EE]" },
            ].map((row, i) => (
              <div
                key={i}
                className="flex items-center gap-2.5 rounded-[9px] border border-[var(--line)] p-2.5"
              >
                <div className={`h-6 w-6 shrink-0 rounded-full ${row.avatar}`} />
                <div className="h-1.5 flex-1 rounded bg-[#EFEEF6]" />
                <div className={`h-[18px] w-10 shrink-0 rounded-[9px] ${row.badge}`} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export async function HomeCaseWorkerSection() {
  const { t } = await getServerTranslator();

  return (
    <section
      className={cn(homeLightSectionShellClass, "text-center")}
      aria-labelledby="home-case-worker-heading"
    >
      <ScrollReveal variant="fade-up">
        <h2
          id="home-case-worker-heading"
          className="font-heading text-[32px] font-extrabold tracking-tight text-foreground sm:text-[38px]"
        >
          {t("home.caseWorkerTitle")}
        </h2>
        <p className={cn(homeSectionSubtitleClass, homeSectionSubtitleMaxWidthClass)}>
          {t("home.caseWorkerSubtitle")}
        </p>
      </ScrollReveal>

      <div className="home-split-grid">
        <ScrollReveal variant="zoom-in" className="home-split-visual">
          <CaseWorkerMock />
        </ScrollReveal>

        <div className="w-full max-w-[572px]">
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
          </div>
          <ScrollReveal variant="fade-up" delay={225}>
            <Link
              href="/contact"
              className="mt-7 inline-flex min-h-[44px] items-center rounded-[10px] bg-foreground px-6 py-3.5 font-heading text-[15px] font-bold text-white transition-opacity hover:opacity-90"
            >
              {t("home.caseWorkerCta")}
            </Link>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
