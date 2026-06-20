import { getAllCategoriesAdmin } from "@/lib/data";
import { AdminCategoriesClient } from "./admin-categories-client";

export default async function AdminCategoriesPage() {
  const categories = await getAllCategoriesAdmin();
  return <AdminCategoriesClient initialCategories={categories} />;
}
