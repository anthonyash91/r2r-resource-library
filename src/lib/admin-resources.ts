import type { ResourceStatus, IntakeSignal } from "@/types";

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
  intake_signals: IntakeSignal[];
  status: string;
  is_featured: boolean;
};

async function parseApiError(
  response: Response,
  fallback: string
): Promise<{ error: string }> {
  const payload = (await response.json().catch(() => ({}))) as { error?: string };
  return { error: payload.error ?? fallback };
}

export async function createResource(
  form: ResourceFormData
): Promise<{ error?: string; id?: string }> {
  const response = await fetch("/api/admin/resources", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form),
  });

  if (!response.ok) {
    const payload = await parseApiError(response, "save_failed");
    if (response.status === 409 && payload.error === "max_featured") {
      return { error: "max_featured" };
    }
    return payload;
  }

  const data = (await response.json()) as { id?: string };
  return { id: data.id };
}

export async function updateResource(
  id: string,
  form: ResourceFormData,
  wasFeatured = false
): Promise<{ error?: string }> {
  const response = await fetch(`/api/admin/resources/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ form, wasFeatured }),
  });

  if (!response.ok) {
    const payload = await parseApiError(response, "save_failed");
    if (response.status === 409 && payload.error === "max_featured") {
      return { error: "max_featured" };
    }
    return payload;
  }

  return {};
}

export async function archiveResourceById(id: string): Promise<{ error?: string }> {
  const response = await fetch(`/api/admin/resources/${id}/archive`, {
    method: "POST",
  });

  if (!response.ok) {
    return parseApiError(response, "save_failed");
  }

  return {};
}

export async function unarchiveResourceById(id: string): Promise<{ error?: string }> {
  const response = await fetch(`/api/admin/resources/${id}/unarchive`, {
    method: "POST",
  });

  if (!response.ok) {
    return parseApiError(response, "save_failed");
  }

  return {};
}

export async function setResourceFeatured(
  id: string,
  featured: boolean,
  currentlyFeatured = false
): Promise<{ error?: string }> {
  const response = await fetch(`/api/admin/resources/${id}/featured`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ featured, currentlyFeatured }),
  });

  if (!response.ok) {
    const payload = await parseApiError(response, "save_failed");
    if (response.status === 409 && payload.error === "max_featured") {
      return { error: "max_featured" };
    }
    return payload;
  }

  return {};
}

export type { ResourceStatus };
