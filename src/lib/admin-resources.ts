import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import type { ResourceStatus } from "@/types";
import { MAX_FEATURED_RESOURCES } from "@/lib/featured-resources-storage";

export function parseListField(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export type ResourceFormData = {
  name: string;
  description: string;
  category_id: string;
  state: string;
  county: string;
  city: string;
  address: string;
  phone: string;
  website: string;
  email: string;
  hours: string;
  eligibility: string;
  notes: string;
  services: string;
  tags: string;
  status: string;
  is_featured: boolean;
};

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
    status: form.status as ResourceStatus,
    served_counties,
    coverage: served_counties.length > 1 ? "multi" : "single",
    is_featured: form.is_featured,
  };
}

async function countActiveFeatured(excludeId?: string): Promise<number> {
  const supabase = createClient();
  if (!supabase) return MAX_FEATURED_RESOURCES;

  let query = supabase
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

export async function canFeatureResource(
  resourceId?: string,
  currentlyFeatured = false
): Promise<boolean> {
  if (currentlyFeatured) return true;
  const count = await countActiveFeatured(resourceId);
  return count < MAX_FEATURED_RESOURCES;
}

export async function createResource(
  form: ResourceFormData
): Promise<{ error?: string; id?: string }> {
  if (!isSupabaseConfigured()) return { error: "unavailable" };

  const supabase = createClient();
  if (!supabase) return { error: "unavailable" };

  if (form.is_featured && !(await canFeatureResource())) {
    return { error: "max_featured" };
  }

  const payload = toDbPayload(form);
  const { data, error } = await supabase.from("resources").insert(payload).select("id").single();

  if (error || !data) return { error: error?.message ?? "save_failed" };
  return { id: data.id as string };
}

export async function updateResource(
  id: string,
  form: ResourceFormData,
  wasFeatured = false
): Promise<{ error?: string }> {
  if (!isSupabaseConfigured()) return { error: "unavailable" };

  const supabase = createClient();
  if (!supabase) return { error: "unavailable" };

  if (form.is_featured && !(await canFeatureResource(id, wasFeatured))) {
    return { error: "max_featured" };
  }

  const payload = toDbPayload(form);
  const { error } = await supabase.from("resources").update(payload).eq("id", id);

  if (error) return { error: error.message };
  return {};
}

export async function archiveResourceById(id: string): Promise<{ error?: string }> {
  if (!isSupabaseConfigured()) return { error: "unavailable" };

  const supabase = createClient();
  if (!supabase) return { error: "unavailable" };

  const { error } = await supabase
    .from("resources")
    .update({ status: "archived", is_featured: false })
    .eq("id", id);

  if (error) return { error: error.message };
  return {};
}

export async function setResourceFeatured(
  id: string,
  featured: boolean,
  currentlyFeatured = false
): Promise<{ error?: string }> {
  if (!isSupabaseConfigured()) return { error: "unavailable" };

  const supabase = createClient();
  if (!supabase) return { error: "unavailable" };

  if (featured && !(await canFeatureResource(id, currentlyFeatured))) {
    return { error: "max_featured" };
  }

  const { error } = await supabase.from("resources").update({ is_featured: featured }).eq("id", id);

  if (error) return { error: error.message };
  return {};
}
