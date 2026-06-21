"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useMemo } from "react";
import { ChevronRight } from "lucide-react";
import { buildBreadcrumbs } from "@/lib/breadcrumbs";
import { useBreadcrumbCurrentLabel } from "@/lib/breadcrumb-context";
import { useTranslations } from "@/i18n/locale-context";
import { cn } from "@/lib/utils";

export function BreadcrumbBar() {
  const pathname = usePathname();
  const { t } = useTranslations();
  const currentLabel = useBreadcrumbCurrentLabel();

  const items = useMemo(
    () => buildBreadcrumbs(pathname, t, currentLabel),
    [pathname, t, currentLabel]
  );

  if (!items) return null;

  return (
    <nav
      aria-label={t("breadcrumb.ariaLabel")}
      className="border-b border-border bg-muted/40 px-4 py-3 sm:px-6 lg:px-8"
    >
      <ol className="mx-auto flex max-w-7xl flex-wrap items-center gap-1.5 text-sm">
        {items.map((item, index) => {
          const isLast = index === items.length - 1;

          return (
            <li key={`${item.href}-${item.label}`} className="flex min-w-0 items-center gap-1.5">
              {index > 0 ? (
                <ChevronRight
                  className="h-4 w-4 shrink-0 text-muted-foreground/70"
                  aria-hidden="true"
                />
              ) : null}
              {isLast ? (
                <span className="truncate font-medium text-foreground" aria-current="page">
                  {item.label}
                </span>
              ) : (
                <Link
                  href={item.href}
                  className={cn(
                    "truncate rounded text-muted-foreground transition-colors hover:text-primary",
                    "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring focus-visible:outline-offset-2"
                  )}
                >
                  {item.label}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
