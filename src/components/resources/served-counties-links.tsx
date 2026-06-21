"use client";

import Link from "next/link";
import type { Resource } from "@/types";
import { buildCountyFilterHref } from "@/lib/resource-coverage";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { useTranslations } from "@/i18n/locale-context";

interface ServedCountiesLinksProps {
  resource: Pick<Resource, "coverage" | "served_counties" | "state">;
}

export function ServedCountiesLinks({ resource }: ServedCountiesLinksProps) {
  const { t } = useTranslations();

  if (resource.coverage === "statewide") {
    return (
      <Link
        href={buildResourcesPageHref({ coverage: "statewide" })}
        className="text-base text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring rounded"
      >
        {t("resources.coverageStatewide")}
      </Link>
    );
  }

  const counties = resource.served_counties ?? [];
  if (counties.length === 0) return null;

  return (
    <p className="text-base leading-relaxed text-muted-foreground">
      {counties.map((county, index) => (
        <span key={county}>
          {index > 0 && ", "}
          <Link
            href={buildCountyFilterHref(county, resource.state)}
            className="text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring rounded"
            aria-label={t("resources.filterByCountyAria", { county })}
          >
            {county}
          </Link>
        </span>
      ))}
    </p>
  );
}
