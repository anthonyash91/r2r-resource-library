import { getAllUsersAdmin } from "@/lib/data";
import { AdminUsersClient } from "./admin-users-client";

export default async function AdminUsersPage() {
  const users = await getAllUsersAdmin();
  return <AdminUsersClient initialUsers={users} />;
}
