import { ResourcesPageSkeleton } from "@/components/resources/resources-page-skeleton";
import { getServerTranslator } from "@/i18n/server";

export default async function ResourcesLoading() {
  const { t } = await getServerTranslator();

  return <ResourcesPageSkeleton loadingLabel={t("resources.loadingAria")} />;
}
