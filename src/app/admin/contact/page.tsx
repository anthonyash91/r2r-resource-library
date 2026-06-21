import { getContactContentAdmin } from "@/lib/data";
import { ContactPageEditor } from "./contact-page-editor";

export default async function AdminContactPage() {
  const initial = await getContactContentAdmin();
  return <ContactPageEditor initial={initial} />;
}
