import Link from "next/link";
import { Briefcase, GraduationCap, Home, ShieldCheck } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { homeLightSectionShellClass, homeSectionSubtitleClass, homeSectionSubtitleMaxWidthClass } from "@/components/home/home-section-divider";
import { cn } from "@/lib/utils";
import { ScrollReveal } from "@/components/ui/scroll-reveal";

const SERVICE_CARDS = [
  {
    slug: "housing",
    icon: Home,
    iconBg: "bg-[#EFEAFE]",
    iconColor: "text-[#5A3FC7]",
    titleKey: "categories.housing.name",
    descKey: "home.serviceHousingDesc",
  },
  {
    slug: "employment",
    icon: Briefcase,
    iconBg: "bg-[#FFE7E0]",
    iconColor: "text-[#E0593F]",
    titleKey: "categories.employment.name",
    descKey: "home.serviceEmploymentDesc",
  },
  {
    slug: "substance-abuse-recovery",
    icon: GraduationCap,
    iconBg: "bg-[#E4F6EE]",
    iconColor: "text-[#2E9C6E]",
    titleKey: "home.serviceRecoveryTitle",
    descKey: "home.serviceRecoveryDesc",
  },
  {
    slug: "legal-aid",
    icon: ShieldCheck,
    iconBg: "bg-[#FFF3D6]",
    iconColor: "text-[#C79114]",
    titleKey: "home.serviceLegalTitle",
    descKey: "home.serviceLegalDesc",
  },
] as const;

export async function HomeServicesSection() {
  const { t } = await getServerTranslator();

  return (
    <section
      className={cn(homeLightSectionShellClass, "text-center")}
      aria-labelledby="home-services-heading"
    >
      <ScrollReveal variant="fade-up">
        <h2
          id="home-services-heading"
          className="font-heading text-[32px] font-extrabold tracking-tight text-foreground sm:text-[38px]"
        >
          {t("home.servicesTitle")}
        </h2>
        <p className={cn(homeSectionSubtitleClass, homeSectionSubtitleMaxWidthClass)}>
          {t("home.servicesSubtitle")}
        </p>
      </ScrollReveal>

      <div className="grid gap-5 text-left sm:grid-cols-2 lg:grid-cols-4">
        {SERVICE_CARDS.map(({ slug, icon: Icon, iconBg, iconColor, titleKey, descKey }, index) => (
          <ScrollReveal key={slug} variant="fade-up" delay={index * 75}>
            <Link
              href={buildResourcesPageHref({ category: slug }, "results")}
              className="block rounded-xl px-1.5 py-2"
            >
              <div
                className={`mb-5 flex h-[50px] w-[50px] items-center justify-center rounded-[13px] ${iconBg}`}
              >
                <Icon className={`h-6 w-6 ${iconColor}`} strokeWidth={1.9} aria-hidden="true" />
              </div>
              <h3 className="font-heading text-[19px] font-bold leading-snug text-foreground">
                {t(titleKey)}
              </h3>
              <p className="mt-2 text-[15px] leading-relaxed text-muted-foreground">{t(descKey)}</p>
              <span className="mt-3.5 inline-block font-heading text-sm font-bold text-[var(--accent-ink)]">
                {t("home.learnMore")}
              </span>
            </Link>
          </ScrollReveal>
        ))}
      </div>
    </section>
  );
}
