import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ResourceDetailView } from "@/components/resources/resource-detail";
import { getResourceById, getRelatedResources } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";

interface PageProps {
  params: Promise<{ id: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { t } = await getServerTranslator();
  const { id } = await params;
  const resource = await getResourceById(id);
  if (!resource) return { title: t("resources.resourceNotFound") };
  return {
    title: resource.name,
    description: resource.description.slice(0, 160),
  };
}

export default async function ResourceDetailPage({ params }: PageProps) {
  const { id } = await params;
  const resource = await getResourceById(id);

  if (!resource || resource.status !== "active") {
    notFound();
  }

  const related = await getRelatedResources(resource);

  return <ResourceDetailView resource={resource} related={related} />;
}
