import { Suspense } from "react";
import type { Metadata } from "next";
import { ResourcesFilterRoot } from "@/components/resources/resources-filter-root";
import {
  ResourcesPageInstantShell,
  ResourcesPageView,
} from "@/components/resources/resources-page-view";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("resources.findResources"),
    description: t("resources.metadataDescription"),
  };
}

export default async function ResourcesPage() {
  const { t } = await getServerTranslator();
  const loadingLabel = t("resources.loadingAria");

  return (
    <Suspense fallback={<ResourcesPageInstantShell loadingLabel={loadingLabel} />}>
      <ResourcesFilterRoot>
        <ResourcesPageView loadingLabel={loadingLabel} />
      </ResourcesFilterRoot>
    </Suspense>
  );
}
