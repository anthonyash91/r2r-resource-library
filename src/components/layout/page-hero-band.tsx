import type { LucideIcon } from "lucide-react";
import { cn, pageHeroPadding } from "@/lib/utils";

interface PageHeroBandProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function PageHeroBand({ icon: Icon, title, description }: PageHeroBandProps) {
  return (
    <section
      className={cn(
        "app-hero-surface relative overflow-hidden px-4 sm:px-6 lg:px-8",
        pageHeroPadding
      )}
    >
      <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div className="absolute -bottom-20 -left-20 h-56 w-56 rounded-full bg-primary-foreground/10 blur-3xl" />
        <div className="absolute -right-16 top-6 h-48 w-48 rounded-full bg-primary-foreground/10 blur-3xl" />
      </div>

      <div className="relative mx-auto max-w-3xl text-center">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-foreground/15 text-primary-foreground ring-1 ring-primary-foreground/20">
          <Icon className="h-7 w-7" aria-hidden="true" />
        </div>
        <h1 className="mb-3 text-3xl font-bold text-primary-foreground sm:text-4xl">{title}</h1>
        <p className="mx-auto max-w-2xl text-base leading-relaxed text-primary-foreground/90 sm:text-lg">
          {description}
        </p>
      </div>
    </section>
  );
}
