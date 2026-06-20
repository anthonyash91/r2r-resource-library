import { getFaqs } from "@/lib/data";
import { AdminFaqsClient } from "./admin-faqs-client";

export default async function AdminFaqsPage() {
  const faqs = await getFaqs();
  return <AdminFaqsClient initial={faqs} />;
}
