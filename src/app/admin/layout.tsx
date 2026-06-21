import { AdminSidebar } from "@/components/admin/admin-sidebar";
import { AdminContentGate } from "@/components/admin/admin-content-gate";
import { AdminSessionGuard } from "@/components/admin/admin-session-guard";
import { requireAdminPageAccess } from "@/lib/admin-auth";

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  await requireAdminPageAccess();

  return (
    <AdminSessionGuard>
      <div className="flex">
        <AdminSidebar />
        <AdminContentGate>{children}</AdminContentGate>
      </div>
    </AdminSessionGuard>
  );
}
