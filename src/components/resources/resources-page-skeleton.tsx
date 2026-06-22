import { cn, pageSectionPadding, resourcesHeroPadding, sectionStackGap } from "@/lib/utils";

interface ResourcesPageSkeletonProps {
  loadingLabel: string;
}

function ResourceCardSkeleton() {
  return (
    <div className="rounded-xl border border-border bg-card p-6">
      <div className="mb-3 flex flex-wrap gap-2">
        <div className="h-6 w-24 animate-pulse rounded-lg bg-muted" />
        <div className="h-6 w-20 animate-pulse rounded-lg bg-muted" />
      </div>
      <div className="mb-2 h-6 w-3/4 animate-pulse rounded bg-muted" />
      <div className="mb-4 space-y-2">
        <div className="h-4 w-full animate-pulse rounded bg-muted" />
        <div className="h-4 w-5/6 animate-pulse rounded bg-muted" />
      </div>
      <div className="space-y-2">
        <div className="h-4 w-2/3 animate-pulse rounded bg-muted" />
        <div className="h-4 w-1/2 animate-pulse rounded bg-muted" />
      </div>
    </div>
  );
}

export function ResourcesPageSkeleton({ loadingLabel }: ResourcesPageSkeletonProps) {
  return (
    <>
      <section
        className={cn(
          "app-hero-surface relative overflow-hidden px-4 sm:px-6 lg:px-8",
          resourcesHeroPadding
        )}
        aria-hidden="true"
      >
        <div className="mx-auto flex w-full max-w-4xl flex-col items-center gap-4 text-center sm:gap-5">
          <div className="w-full space-y-3">
            <div className="mx-auto h-9 w-64 max-w-full animate-pulse rounded-lg bg-primary-foreground/20 sm:h-10 sm:w-80" />
            <div className="mx-auto h-5 w-full max-w-2xl animate-pulse rounded bg-primary-foreground/15" />
            <div className="mx-auto h-5 w-5/6 max-w-xl animate-pulse rounded bg-primary-foreground/15" />
          </div>
          <div className="h-12 w-full max-w-3xl animate-pulse rounded-full bg-primary-foreground/25 sm:h-14" />
        </div>
      </section>

      <div className={cn("app-band-alt", pageSectionPadding)}>
        <div
          className={cn("mx-auto max-w-7xl", sectionStackGap)}
          role="status"
          aria-live="polite"
          aria-busy="true"
          aria-label={loadingLabel}
        >
          <div className="h-12 animate-pulse rounded-xl border border-border bg-card" />
          <div className="h-5 w-56 animate-pulse rounded bg-muted" />
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, index) => (
              <ResourceCardSkeleton key={index} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
