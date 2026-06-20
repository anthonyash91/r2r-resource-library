import { getAnnouncements } from "@/lib/data";
import { AdminAnnouncementsClient } from "./admin-announcements-client";

export default async function AdminAnnouncementsPage() {
  const announcements = await getAnnouncements();
  return <AdminAnnouncementsClient initial={announcements} />;
}
