import Link from "next/link";
import type { Resource } from "@/types";
import { getServerTranslator } from "@/i18n/server";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { homeLightSectionShellClass, homeSectionSubtitleClass, homeSectionSubtitleWideMaxWidthClass } from "@/components/home/home-section-divider";
import { cn } from "@/lib/utils";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { HomeFeaturedResourcesGrid } from "@/components/home/home-featured-resources-grid";

interface HomeFeaturedResourcesSectionProps {
  resources: Resource[];
}

export async function HomeFeaturedResourcesSection({
  resources,
}: HomeFeaturedResourcesSectionProps) {
  const { t } = await getServerTranslator();
  const featured = resources.slice(0, 3);

  if (featured.length === 0) return null;

  return (
    <section
      className={cn(homeLightSectionShellClass, "pb-[77px]")}
      aria-labelledby="home-featured-resources-heading"
    >
      <div className="text-center">
        <ScrollReveal variant="fade-up">
          <h2
            id="home-featured-resources-heading"
            className="font-heading text-[32px] font-extrabold tracking-tight text-foreground sm:text-[38px]"
          >
            {t("home.featuredTitle")}
          </h2>
          <p className={cn(homeSectionSubtitleClass, homeSectionSubtitleWideMaxWidthClass)}>
            {t("home.featuredSubtitle")}
          </p>
        </ScrollReveal>
      </div>

      <HomeFeaturedResourcesGrid resources={featured} />

      <ScrollReveal variant="fade-up" delay={225}>
        <div className="mt-9 text-center">
          <Link
            href={buildResourcesPageHref()}
            className="inline-flex min-h-[44px] items-center rounded-[10px] bg-[#EFEAFE] px-7 py-[15px] font-heading text-[15px] font-bold leading-none text-[var(--accent-ink)] transition-opacity hover:opacity-90"
          >
            {t("home.viewAllResourcesArrow")}
          </Link>
        </div>
      </ScrollReveal>
    </section>
  );
}
