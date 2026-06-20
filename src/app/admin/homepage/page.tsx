import { getHomepageContent, getAllResourcesAdmin } from "@/lib/data";
import { HomepageEditor } from "./homepage-editor";

export default async function AdminHomepagePage() {
  const [content, resources] = await Promise.all([
    getHomepageContent(),
    getAllResourcesAdmin(),
  ]);
  return <HomepageEditor initial={content} resources={resources} />;
}
