import { getCmsPages } from "@/lib/data";
import { AdminCmsClient } from "./admin-cms-client";

export default async function AdminCmsPage() {
  const pages = await getCmsPages();
  return <AdminCmsClient initialPages={pages} />;
}
