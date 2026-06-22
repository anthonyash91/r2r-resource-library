import type { SupabaseClient } from "@supabase/supabase-js";

export type DeleteUserMethod = "auth_api" | "rpc";

export interface DeleteUserResult {
  success: boolean;
  method?: DeleteUserMethod;
  error?: string;
}

async function cleanupUserData(
  admin: SupabaseClient,
  targetUserId: string
): Promise<string | null> {
  const { error: savesError } = await admin
    .from("saved_resources")
    .delete()
    .eq("user_id", targetUserId);
  if (savesError) {
    return `saved_resources: ${savesError.message}`;
  }

  const { error: viewsError } = await admin
    .from("resource_views")
    .delete()
    .eq("user_id", targetUserId);
  if (viewsError) {
    return `resource_views: ${viewsError.message}`;
  }

  const { error: profileError } = await admin.from("profiles").delete().eq("id", targetUserId);
  if (profileError) {
    return `profiles: ${profileError.message}`;
  }

  return null;
}

export async function deleteUserAccount(
  admin: SupabaseClient,
  targetUserId: string
): Promise<DeleteUserResult> {
  const cleanupError = await cleanupUserData(admin, targetUserId);
  if (cleanupError) {
    return { success: false, error: cleanupError };
  }

  const { error: deleteError } = await admin.auth.admin.deleteUser(targetUserId, false);

  if (!deleteError) {
    return { success: true, method: "auth_api" };
  }

  const { error: rpcError } = await admin.rpc("admin_delete_user_account", {
    target_user_id: targetUserId,
  });

  if (!rpcError) {
    return { success: true, method: "rpc" };
  }

  return {
    success: false,
    error: [deleteError.message, `rpc: ${rpcError.message}`].filter(Boolean).join("; "),
  };
}
