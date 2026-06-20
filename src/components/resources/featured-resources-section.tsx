"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Resource } from "@/types";
import { ResourceCard } from "@/components/resources/resource-card";
import { resolveFeaturedResources } from "@/lib/featured-resources-storage";
import { useTranslations } from "@/i18n/locale-context";

interface FeaturedResourcesSectionProps {
  resources: Resource[];
}

export function FeaturedResourcesSection({ resources }: FeaturedResourcesSectionProps) {
  const { t } = useTranslations();
  const [featured, setFeatured] = useState<Resource[]>(() => resolveFeaturedResources(resources));

  useEffect(() => {
    const syncFeatured = () => {
      setFeatured(resolveFeaturedResources(resources));
    };

    syncFeatured();
    window.addEventListener("featured-resources-updated", syncFeatured);
    window.addEventListener("storage", syncFeatured);

    return () => {
      window.removeEventListener("featured-resources-updated", syncFeatured);
      window.removeEventListener("storage", syncFeatured);
    };
  }, [resources]);

  if (featured.length === 0) return null;

  return (
    <section
      className="border-y border-border bg-card px-4 py-16 sm:px-6 lg:px-8 lg:py-20"
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
          {featured.map((resource) => (
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
