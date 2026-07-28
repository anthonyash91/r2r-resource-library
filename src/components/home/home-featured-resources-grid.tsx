"use client";

import type { Resource } from "@/types";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { HomeFeaturedResourceCard } from "@/components/home/home-featured-resource-card";

interface HomeFeaturedResourcesGridProps {
  resources: Resource[];
}

export function HomeFeaturedResourcesGrid({ resources }: HomeFeaturedResourcesGridProps) {
  return (
    <div className="columns-1 gap-[18px] md:columns-2 lg:columns-3">
      {resources.map((resource, index) => (
        <ScrollReveal
          key={resource.id}
          variant="fade-up"
          delay={index * 75}
          className="mb-[18px] block w-full max-w-full break-inside-avoid"
        >
          <HomeFeaturedResourceCard resource={resource} />
        </ScrollReveal>
      ))}
    </div>
  );
}
