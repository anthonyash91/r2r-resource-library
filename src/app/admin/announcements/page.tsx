import { getAllAnnouncementsAdmin } from "@/lib/data";
import { AdminAnnouncementsClient } from "./admin-announcements-client";

export default async function AdminAnnouncementsPage() {
  const announcements = await getAllAnnouncementsAdmin();
  return <AdminAnnouncementsClient initial={announcements} />;
}
