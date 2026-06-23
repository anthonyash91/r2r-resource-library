import { createAdminClient } from "@/lib/supabase/admin";
import type { ResourceStatus } from "@/types";
import { MAX_FEATURED_RESOURCES } from "@/lib/featured-resources-storage";
import {
  parseListField,
  type ResourceFormData,
} from "@/lib/admin-resources";

function toDbPayload(form: ResourceFormData) {
  const county = form.county.trim();
  const served_counties = county ? [county] : [];

  return {
    name: form.name.trim(),
    description: form.description.trim(),
    category_id: form.category_id,
    state: form.state.trim() || null,
    county: county || null,
    city: form.city.trim() || null,
    address: form.address.trim() || null,
    phone: form.phone.trim() || null,
    website: form.website.trim() || null,
    email: form.email.trim() || null,
    hours: form.hours.trim() || null,
    eligibility: form.eligibility.trim() || null,
    notes: form.notes.trim() || null,
    services: parseListField(form.services),
    tags: parseListField(form.tags),
    intake_signals: form.intake_signals,
    status: form.status as ResourceStatus,
    served_counties,
    coverage: served_counties.length > 1 ? "multi" : "single",
    is_featured: form.is_featured,
  };
}

async function countActiveFeatured(
  excludeId?: string
): Promise<number> {
  const admin = createAdminClient();
  if (!admin) return MAX_FEATURED_RESOURCES;

  let query = admin
    .from("resources")
    .select("id", { count: "exact", head: true })
    .eq("status", "active")
    .eq("is_featured", true);

  if (excludeId) {
    query = query.neq("id", excludeId);
  }

  const { count } = await query;
  return count ?? 0;
}

async function canFeatureResource(
  resourceId?: string,
  currentlyFeatured = false
): Promise<boolean> {
  if (currentlyFeatured) return true;
  const count = await countActiveFeatured(resourceId);
  return count < MAX_FEATURED_RESOURCES;
}

export async function createResourceServer(
  form: ResourceFormData
): Promise<{ error?: string; id?: string }> {
  const admin = createAdminClient();
  if (!admin) return { error: "unavailable" };

  if (form.is_featured && !(await canFeatureResource())) {
    return { error: "max_featured" };
  }

  const { data, error } = await admin
    .from("resources")
    .insert(toDbPayload(form))
    .select("id")
    .single();

  if (error || !data) return { error: error?.message ?? "save_failed" };
  return { id: data.id as string };
}

export async function updateResourceServer(
  id: string,
  form: ResourceFormData,
  wasFeatured = false
): Promise<{ error?: string }> {
  const admin = createAdminClient();
  if (!admin) return { error: "unavailable" };

  if (form.is_featured && !(await canFeatureResource(id, wasFeatured))) {
    return { error: "max_featured" };
  }

  const { error } = await admin.from("resources").update(toDbPayload(form)).eq("id", id);
  if (error) return { error: error.message };
  return {};
}

export async function archiveResourceByIdServer(id: string): Promise<{ error?: string }> {
  const admin = createAdminClient();
  if (!admin) return { error: "unavailable" };

  const { error } = await admin
    .from("resources")
    .update({ status: "archived", is_featured: false })
    .eq("id", id);

  if (error) return { error: error.message };
  return {};
}

export async function unarchiveResourceByIdServer(id: string): Promise<{ error?: string }> {
  const admin = createAdminClient();
  if (!admin) return { error: "unavailable" };

  const { error } = await admin
    .from("resources")
    .update({ status: "active" })
    .eq("id", id);

  if (error) return { error: error.message };
  return {};
}

export async function setResourceFeaturedServer(
  id: string,
  featured: boolean,
  currentlyFeatured = false
): Promise<{ error?: string }> {
  const admin = createAdminClient();
  if (!admin) return { error: "unavailable" };

  if (featured && !(await canFeatureResource(id, currentlyFeatured))) {
    return { error: "max_featured" };
  }

  const { error } = await admin.from("resources").update({ is_featured: featured }).eq("id", id);
  if (error) return { error: error.message };
  return {};
}
