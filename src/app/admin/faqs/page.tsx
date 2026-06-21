import { getAllFaqsAdmin } from "@/lib/data";
import { AdminFaqsClient } from "./admin-faqs-client";

export default async function AdminFaqsPage() {
  const faqs = await getAllFaqsAdmin();
  return <AdminFaqsClient initial={faqs} />;
}
