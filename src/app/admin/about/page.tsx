import { getAboutContentAdmin } from "@/lib/data";
import { AboutPageEditor } from "./about-page-editor";

export default async function AdminAboutPage() {
  const initial = await getAboutContentAdmin();
  return <AboutPageEditor initial={initial} />;
}
