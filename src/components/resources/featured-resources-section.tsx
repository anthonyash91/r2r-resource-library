import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceCard } from "@/components/resources/resource-card";
import { getServerTranslator } from "@/i18n/server";
import { cn, pageSectionPadding } from "@/lib/utils";

interface FeaturedResourcesSectionProps {
  resources: Resource[];
}

export async function FeaturedResourcesSection({ resources }: FeaturedResourcesSectionProps) {
  const { t } = await getServerTranslator();

  if (resources.length === 0) return null;

  return (
    <section
      className={cn("border-y border-border app-band-muted", pageSectionPadding)}
      aria-labelledby="featured-resources-heading"
    >
      <div className="mx-auto max-w-7xl">
        <header className="mb-10 text-center">
          <h2 id="featured-resources-heading" className="mb-3 text-3xl font-bold text-foreground sm:text-4xl">
            {t("home.featuredTitle")}
          </h2>
          <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
            {t("home.featuredSubtitle")}
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {resources.map((resource) => (
            <ResourceCard key={resource.id} resource={resource} />
          ))}
        </div>

        <div className="mt-10 text-center">
          <Link
            href="/resources"
            className="inline-flex min-h-[48px] cursor-pointer items-center gap-2 text-lg font-semibold text-primary transition-colors hover:text-primary-hover focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
          >
            {t("home.viewAllResources")}
            <ArrowRight className="h-5 w-5" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </section>
  );
}
