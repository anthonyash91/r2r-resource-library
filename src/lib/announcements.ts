import type { Announcement } from "@/types";

/** Whether a published announcement should appear on the public site. */
export function isAnnouncementActive(
  announcement: Pick<Announcement, "status" | "starts_at" | "ends_at">,
  now: Date = new Date()
): boolean {
  if (announcement.status !== "published") return false;

  const time = now.getTime();
  if (announcement.starts_at && new Date(announcement.starts_at).getTime() > time) {
    return false;
  }
  if (announcement.ends_at && new Date(announcement.ends_at).getTime() <= time) {
    return false;
  }

  return true;
}

/** End of the selected calendar day in local time, stored as ISO UTC. */
export function dateInputToEndsAt(dateStr: string): string {
  const [year, month, day] = dateStr.split("-").map(Number);
  return new Date(year, month - 1, day, 23, 59, 59, 999).toISOString();
}

export function isExpirationDateInPast(dateStr: string, now: Date = new Date()): boolean {
  return new Date(dateInputToEndsAt(dateStr)).getTime() <= now.getTime();
}
