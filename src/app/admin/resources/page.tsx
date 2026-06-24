import { getAllCategoriesAdmin, getAllResourcesAdmin } from "@/lib/data";
import { AdminResourcesClient } from "./admin-resources-client";

export default async function AdminResourcesPage() {
  const [resources, categories] = await Promise.all([
    getAllResourcesAdmin(),
    getAllCategoriesAdmin(),
  ]);
  return <AdminResourcesClient initialResources={resources} categories={categories} />;
}
