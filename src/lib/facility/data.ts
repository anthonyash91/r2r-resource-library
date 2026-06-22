import type { SupabaseClient } from "@supabase/supabase-js";
import { createAdminClient } from "@/lib/supabase/admin";
import { preferencesFromProfile } from "@/lib/user-preferences/parse";
import type { UserPreferences } from "@/lib/user-preferences/types";
import {
  decryptSiteId,
  hashInmatePin,
  hashSiteId,
  maskSiteId,
} from "@/lib/facility/crypto";

export interface FacilityRecord {
  id: string;
  name: string;
  site_id_hash: string;
  site_id_encrypted: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface FacilityListItem {
  id: string;
  name: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
  siteIdMasked: string;
  signupCount: number;
}

export async function getFacilityById(facilityId: string): Promise<FacilityRecord | null> {
  const supabase = createAdminClient();
  if (!supabase) return null;

  const { data, error } = await supabase
    .from("facilities")
    .select("*")
    .eq("id", facilityId)
    .maybeSingle();

  if (error || !data) return null;
  return data as FacilityRecord;
}

export async function getFacilityProfileByPinHash(
  facilityId: string,
  pinHash: string
): Promise<{ id: string; email: string; contact_email: string | null } | null> {
  const supabase = createAdminClient();
  if (!supabase) return null;

  const { data, error } = await supabase
    .from("profiles")
    .select("id, email, contact_email")
    .eq("facility_id", facilityId)
    .eq("inmate_pin_hash", pinHash)
    .eq("signup_context", "facility")
    .maybeSingle();

  if (error || !data) return null;
  return data as { id: string; email: string; contact_email: string | null };
}

export async function getFacilityProfilePreferencesByPinHash(
  facilityId: string,
  pinHash: string
): Promise<UserPreferences | null> {
  const supabase = createAdminClient();
  if (!supabase) return null;

  const { data, error } = await supabase
    .from("profiles")
    .select("state, county, priority_categories, onboarding_completed_at")
    .eq("facility_id", facilityId)
    .eq("inmate_pin_hash", pinHash)
    .maybeSingle();

  if (error || !data) return null;
  return preferencesFromProfile(data);
}

export async function findFacilityBySiteId(siteId: string): Promise<FacilityRecord | null> {
  const supabase = createAdminClient();
  if (!supabase) return null;

  const siteIdHash = hashSiteId(siteId);
  const { data, error } = await supabase
    .from("facilities")
    .select("*")
    .eq("site_id_hash", siteIdHash)
    .eq("is_active", true)
    .maybeSingle();

  if (error || !data) return null;
  return data as FacilityRecord;
}

export async function facilityAccountExists(
  facilityId: string,
  pin: string
): Promise<boolean> {
  const supabase = createAdminClient();
  if (!supabase) return false;

  const pinHash = hashInmatePin(facilityId, pin);
  const { data, error } = await supabase
    .from("profiles")
    .select("id")
    .eq("facility_id", facilityId)
    .eq("inmate_pin_hash", pinHash)
    .maybeSingle();

  return !error && Boolean(data);
}

export async function getFacilityProfileRecoveryByPinHash(
  facilityId: string,
  pinHash: string
): Promise<{
  id: string;
  email: string;
  recovery_question_1: string;
  recovery_question_2: string;
  recovery_answer_1_hash: string;
  recovery_answer_2_hash: string;
} | null> {
  const supabase = createAdminClient();
  if (!supabase) return null;

  const { data, error } = await supabase
    .from("profiles")
    .select(
      "id, email, recovery_question_1, recovery_question_2, recovery_answer_1_hash, recovery_answer_2_hash"
    )
    .eq("facility_id", facilityId)
    .eq("inmate_pin_hash", pinHash)
    .eq("signup_context", "facility")
    .maybeSingle();

  if (error || !data) return null;
  return data as {
    id: string;
    email: string;
    recovery_question_1: string;
    recovery_question_2: string;
    recovery_answer_1_hash: string;
    recovery_answer_2_hash: string;
  };
}

export async function facilityAccountExistsByPinHash(
  facilityId: string,
  pinHash: string
): Promise<boolean> {
  const supabase = createAdminClient();
  if (!supabase) return false;

  const { data, error } = await supabase
    .from("profiles")
    .select("id")
    .eq("facility_id", facilityId)
    .eq("inmate_pin_hash", pinHash)
    .maybeSingle();

  return !error && Boolean(data);
}

export async function listFacilitiesWithCounts(
  supabase: SupabaseClient
): Promise<FacilityListItem[]> {
  const { data: facilities, error } = await supabase
    .from("facilities")
    .select("*")
    .order("name");

  if (error || !facilities) return [];

  const { data: profiles } = await supabase
    .from("profiles")
    .select("facility_id")
    .not("facility_id", "is", null);

  const counts = new Map<string, number>();
  for (const row of profiles ?? []) {
    const id = row.facility_id as string;
    counts.set(id, (counts.get(id) ?? 0) + 1);
  }

  return (facilities as FacilityRecord[]).map((facility) => {
    let siteIdMasked = "••••";
    try {
      siteIdMasked = maskSiteId(decryptSiteId(facility.site_id_encrypted));
    } catch {
      siteIdMasked = "••••";
    }

    return {
      id: facility.id,
      name: facility.name,
      isActive: facility.is_active,
      createdAt: facility.created_at,
      updatedAt: facility.updated_at,
      siteIdMasked,
      signupCount: counts.get(facility.id) ?? 0,
    };
  });
}

export async function getFacilitySiteIdForAdmin(
  facilityId: string,
  supabase: SupabaseClient
): Promise<string | null> {
  const { data, error } = await supabase
    .from("facilities")
    .select("site_id_encrypted")
    .eq("id", facilityId)
    .maybeSingle();

  if (error || !data) return null;

  try {
    return decryptSiteId(data.site_id_encrypted as string);
  } catch {
    return null;
  }
}

export async function verifyFacilityProfileBinding(
  userId: string,
  facilityId: string,
  pinHash: string
): Promise<boolean> {
  const supabase = createAdminClient();
  if (!supabase) return false;

  const { data, error } = await supabase
    .from("profiles")
    .select("facility_id, inmate_pin_hash, signup_context")
    .eq("id", userId)
    .maybeSingle();

  if (error || !data) return false;
  if (data.signup_context !== "facility") return false;
  return data.facility_id === facilityId && data.inmate_pin_hash === pinHash;
}
