import type { Metadata } from "next";
import { DashboardClient } from "./dashboard-client";
import { getCategories, getResources } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("dashboard.title"),
    description: t("dashboard.description"),
  };
}

export default async function DashboardPage() {
  const [categories, allResources] = await Promise.all([
    getCategories(),
    getResources(),
  ]);

  const recommended = [...allResources]
    .sort((a, b) => b.view_count - a.view_count)
    .slice(0, 6);

  return <DashboardClient categories={categories} recommended={recommended} />;
}
