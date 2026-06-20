import { getAllCategoriesAdmin } from "@/lib/data";
import { ResourceForm } from "@/components/admin/resource-form";
import { getServerTranslator } from "@/i18n/server";

export default async function NewResourcePage() {
  const { t } = await getServerTranslator();
  const categories = await getAllCategoriesAdmin();

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.addResourceTitle")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.resourceManagementDesc")}</p>
      </header>
      <ResourceForm categories={categories} />
    </div>
  );
}
