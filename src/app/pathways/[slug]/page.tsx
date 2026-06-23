import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { PathwayView } from "@/components/pathways/pathway-view";
import { getResources } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";
import { getPathwayBySlug, matchPathwaySteps } from "@/lib/pathways";
import { getServerUserPreferences } from "@/lib/user-preferences/server";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const pathway = getPathwayBySlug(slug);
  const { t } = await getServerTranslator();

  if (!pathway) {
    return { title: t("pathways.notFoundTitle") };
  }

  return {
    title: t("pathways.firstWeek.title"),
    description: t("pathways.firstWeek.metaDescription"),
  };
}

export default async function PathwayPage({ params }: PageProps) {
  const { slug } = await params;
  const pathway = getPathwayBySlug(slug);

  if (!pathway) {
    notFound();
  }

  const [resources, preferences] = await Promise.all([
    getResources(),
    getServerUserPreferences(),
  ]);

  const matchedSteps = matchPathwaySteps(resources, pathway, preferences);

  return (
    <PathwayView slug={slug} matchedSteps={matchedSteps} preferences={preferences} />
  );
}
