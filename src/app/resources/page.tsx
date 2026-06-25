import { Suspense } from "react";
import type { Metadata } from "next";
import { ResourcesFilterRoot } from "@/components/resources/resources-filter-root";
import {
  ResourcesPageInstantShell,
  ResourcesPageView,
} from "@/components/resources/resources-page-view";
import { getServerTranslator } from "@/i18n/server";
import {
  getResourcesBootstrap,
  resolveEffectiveResourcesPageParams,
  searchParamsFromPageProps,
} from "@/lib/resources-bootstrap";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { resourcesPageParamsFromSearchParams } from "@/lib/resources-page-filters";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("resources.findResources"),
    description: t("resources.metadataDescription"),
  };
}

interface ResourcesPageProps {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}

export default async function ResourcesPage({ searchParams }: ResourcesPageProps) {
  const { t } = await getServerTranslator();
  const loadingLabel = t("resources.loadingAria");
  const rawParams = await searchParams;
  const urlParams = resourcesPageParamsFromSearchParams(searchParamsFromPageProps(rawParams));
  const preferences = await getServerUserPreferences();
  const effectiveParams = resolveEffectiveResourcesPageParams(urlParams, preferences);
  const initialBootstrap = await getResourcesBootstrap(effectiveParams);

  return (
    <Suspense fallback={<ResourcesPageInstantShell loadingLabel={loadingLabel} />}>
      <ResourcesFilterRoot initialAppliedParams={effectiveParams}>
        <ResourcesPageView
          loadingLabel={loadingLabel}
          initialBootstrap={initialBootstrap}
        />
      </ResourcesFilterRoot>
    </Suspense>
  );
}
