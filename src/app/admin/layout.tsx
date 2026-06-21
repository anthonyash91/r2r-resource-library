import { AdminSidebar } from "@/components/admin/admin-sidebar";
import { AdminContentGate } from "@/components/admin/admin-content-gate";
import { AdminSessionGuard } from "@/components/admin/admin-session-guard";
import { requireAdminPageAccess } from "@/lib/admin-auth";
import { isSupabaseConfigured } from "@/lib/supabase/server";

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  if (isSupabaseConfigured()) {
    await requireAdminPageAccess();
  }

  return (
    <AdminSessionGuard>
      <div className="flex">
        <AdminSidebar />
        <AdminContentGate>{children}</AdminContentGate>
      </div>
    </AdminSessionGuard>
  );
}
