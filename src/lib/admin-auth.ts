import type { SupabaseClient } from "@supabase/supabase-js";
import { redirect } from "next/navigation";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";

export async function getAdminSession(
  supabase: SupabaseClient
): Promise<{ userId: string } | null> {
  const {
    data: { user },
    error: authError,
  } = await supabase.auth.getUser();

  if (authError || !user) {
    return null;
  }

  const { data: profile, error: profileError } = await supabase
    .from("profiles")
    .select("role")
    .eq("id", user.id)
    .single();

  if (profileError || profile?.role !== "admin") {
    return null;
  }

  return { userId: user.id };
}

export async function requireAdminPageAccess(): Promise<{ userId: string }> {
  if (!isSupabaseConfigured()) {
    redirect("/login?next=/admin");
  }

  const supabase = await createClient();
  if (!supabase) {
    redirect("/login?next=/admin");
  }

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login?next=/admin");
  }

  const session = await getAdminSession(supabase);
  if (!session) {
    redirect("/dashboard");
  }

  return session;
}
