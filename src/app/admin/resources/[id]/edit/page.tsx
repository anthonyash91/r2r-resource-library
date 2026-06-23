import { notFound } from "next/navigation";
import { getResourceById, getAllCategoriesAdmin } from "@/lib/data";
import { ResourceForm } from "@/components/admin/resource-form";
import { getServerTranslator } from "@/i18n/server";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function EditResourcePage({ params }: PageProps) {
  const { t } = await getServerTranslator();
  const { id } = await params;
  const [resource, categories] = await Promise.all([
    getResourceById(id),
    getAllCategoriesAdmin(),
  ]);

  if (!resource) notFound();

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.editResourceTitle")}</h1>
        <p className="text-lg text-muted-foreground">{resource.name}</p>
      </header>
      <ResourceForm
        categories={categories}
        resource={{
          id: resource.id,
          name: resource.name,
          description: resource.description,
          category_id: resource.category_id,
          state: resource.state ?? "",
          county: resource.county ?? "",
          city: resource.city ?? "",
          address: resource.address ?? "",
          phone: resource.phone ?? "",
          website: resource.website ?? "",
          email: resource.email ?? "",
          hours: resource.hours ?? "",
          eligibility: resource.eligibility ?? "",
          notes: resource.notes ?? "",
          services: resource.services.join(", "),
          tags: resource.tags.join(", "),
          intake_signals: resource.intake_signals ?? [],
          status: resource.status,
          is_featured: resource.is_featured,
        }}
      />
    </div>
  );
}
