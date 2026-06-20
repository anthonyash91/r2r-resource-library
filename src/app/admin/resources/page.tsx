import { getAllResourcesAdmin } from "@/lib/data";
import { AdminResourcesClient } from "./admin-resources-client";

export default async function AdminResourcesPage() {
  const resources = await getAllResourcesAdmin();
  return <AdminResourcesClient initialResources={resources} />;
}
