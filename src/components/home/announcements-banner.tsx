import { Megaphone } from "lucide-react";
import type { Announcement } from "@/types";

interface AnnouncementsBannerProps {
  announcements: Announcement[];
}

export function AnnouncementsBanner({ announcements }: AnnouncementsBannerProps) {
  const pinned = announcements.filter((item) => item.is_pinned);
  if (pinned.length === 0) return null;

  return (
    <div className="border-b border-border bg-accent/10 px-4 py-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl space-y-3">
        {pinned.map((announcement) => (
          <div
            key={announcement.id}
            className="flex gap-3 rounded-xl border border-accent/30 bg-card px-4 py-3 sm:px-5"
          >
            <Megaphone className="mt-0.5 h-5 w-5 shrink-0 text-accent" aria-hidden="true" />
            <div>
              <p className="font-semibold text-foreground">{announcement.title}</p>
              <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
                {announcement.content}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
