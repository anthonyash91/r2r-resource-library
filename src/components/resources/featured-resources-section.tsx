import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Button } from "@/components/ui/button";
import { getServerTranslator } from "@/i18n/server";
import { cn, pageSectionPadding, pageSectionHeadingClass, pageSectionSubtitleClass, pageSectionBandClass, type PageSectionBand } from "@/lib/utils";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { ScrollReveal } from "@/components/ui/scroll-reveal";

interface FeaturedResourcesSectionProps {
  resources: Resource[];
  band?: PageSectionBand;
}

export async function FeaturedResourcesSection({
  resources,
  band = "muted",
}: FeaturedResourcesSectionProps) {
  const { t } = await getServerTranslator();

  if (resources.length === 0) return null;

  return (
    <section
      className={cn(pageSectionBandClass(band), pageSectionPadding)}
      aria-labelledby="featured-resources-heading"
    >
      <div className="mx-auto max-w-7xl">
        <ScrollReveal variant="blur-up">
          <header className="mb-10 text-center">
            <h2 id="featured-resources-heading" className={cn("mb-3 text-foreground", pageSectionHeadingClass)}>
              {t("home.featuredTitle")}
            </h2>
            <p className={cn("mx-auto max-w-2xl", pageSectionSubtitleClass)}>
              {t("home.featuredSubtitle")}
            </p>
          </header>
        </ScrollReveal>

        <ResourceMasonry resources={resources} columns={3} contained />

        <ScrollReveal variant="fade-up" delay={240}>
          <div className="mt-10 flex justify-center">
            <Link href={buildResourcesPageHref()}>
              <Button size="lg" variant="outline" className="gap-2">
                {t("home.viewAllResources")}
                <ArrowRight className="h-5 w-5" aria-hidden="true" />
              </Button>
            </Link>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
