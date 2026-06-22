import type { Metadata } from "next";
import { DashboardClient } from "./dashboard-client";
import { getCategories, getResources } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";
import { getRecommendedResources } from "@/lib/user-preferences/recommendations";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("dashboard.title"),
    description: t("dashboard.description"),
  };
}

export default async function DashboardPage() {
  const [categories, allResources, preferences] = await Promise.all([
    getCategories(),
    getResources(),
    getServerUserPreferences(),
  ]);

  const recommended = hasCompletedOnboarding(preferences)
    ? getRecommendedResources(allResources, preferences)
    : [];

  return (
    <DashboardClient
      categories={categories}
      recommended={recommended}
      preferences={preferences}
    />
  );
}
