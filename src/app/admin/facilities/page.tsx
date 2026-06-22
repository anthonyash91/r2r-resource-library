import { AdminFacilitiesClient } from "./admin-facilities-client";
import { requireAdminPageAccess } from "@/lib/admin-auth";
import { listFacilitiesWithCounts } from "@/lib/facility/data";
import { createClient } from "@/lib/supabase/server";
import { getServerTranslator } from "@/i18n/server";
import type { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return { title: t("admin.facilitiesTitle") };
}

export default async function AdminFacilitiesPage() {
  await requireAdminPageAccess();
  const supabase = await createClient();
  const facilities = supabase ? await listFacilitiesWithCounts(supabase) : [];

  return <AdminFacilitiesClient initialFacilities={facilities} />;
}
