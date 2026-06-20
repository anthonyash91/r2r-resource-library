"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import type { Category } from "@/types";
import { CategoryIcon } from "@/lib/category-icons";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";

interface CategoryPillsProps {
  categories: Category[];
  compact?: boolean;
  preserveParams?: boolean;
  activeSlug?: string | null;
  wrap?: boolean;
  className?: string;
}

function PillLink({
  href,
  isActive,
  children,
}: {
  href: string;
  isActive: boolean;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      role="listitem"
      className={cn(
        "inline-flex shrink-0 cursor-pointer items-center justify-center gap-1.5 rounded-full border px-3.5 py-2 text-sm font-medium leading-none transition-colors",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
        isActive
          ? "border-primary bg-primary text-primary-foreground"
          : "border-border bg-card text-foreground hover:border-primary/40 hover:bg-secondary"
      )}
      aria-current={isActive ? "true" : undefined}
    >
      {children}
    </Link>
  );
}

function CategoryPillsList({
  categories,
  compact,
  activeSlug,
  buildHref,
  wrap = false,
}: {
  categories: Category[];
  compact: boolean;
  activeSlug: string | null;
  buildHref: (slug?: string) => string;
  wrap?: boolean;
}) {
  const { t } = useTranslations();

  const categoryLabel = (category: Category) => {
    const key = `categories.${category.slug}.name`;
    const translated = t(key);
    return translated === key ? category.name : translated;
  };

  return (
    <div className={cn(!compact && "mb-0")}>
      {!compact && (
        <p className="mb-2 text-sm font-medium text-muted-foreground">
          {t("resources.browseByCategory")}
        </p>
      )}
      <div
        className={cn(
          "flex gap-2",
          wrap ? "flex-wrap justify-center" : "overflow-x-auto pb-1"
        )}
        role="list"
        aria-label={t("resources.browseByCategory")}
      >
        <PillLink href={buildHref()} isActive={false}>
          {t("common.all")}
        </PillLink>
        {categories.map((category) => (
          <PillLink
            key={category.id}
            href={buildHref(category.slug)}
            isActive={activeSlug === category.slug}
          >
            <CategoryIcon icon={category.icon} className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
            {categoryLabel(category)}
          </PillLink>
        ))}
      </div>
    </div>
  );
}

function CategoryPillsWithParams({
  categories,
  compact,
  wrap,
  className,
}: Omit<CategoryPillsProps, "preserveParams" | "activeSlug">) {
  const searchParams = useSearchParams();
  const activeSlug = searchParams.get("category");

  const buildHref = (slug?: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (slug) {
      params.set("category", slug);
    } else {
      params.delete("category");
    }
    const qs = params.toString();
    return qs ? `/resources?${qs}` : "/resources";
  };

  return (
    <div className={className}>
      <CategoryPillsList
        categories={categories}
        compact={compact ?? false}
        activeSlug={activeSlug}
        buildHref={buildHref}
        wrap={wrap}
      />
    </div>
  );
}

export function CategoryPills({
  categories,
  compact = false,
  preserveParams = false,
  activeSlug = null,
  wrap = false,
  className,
}: CategoryPillsProps) {
  if (preserveParams) {
    return (
      <CategoryPillsWithParams
        categories={categories}
        compact={compact}
        wrap={wrap}
        className={className}
      />
    );
  }

  const buildHref = (slug?: string) =>
    slug ? `/resources?category=${slug}` : "/resources";

  return (
    <div className={className}>
      <CategoryPillsList
        categories={categories}
        compact={compact}
        activeSlug={activeSlug}
        buildHref={buildHref}
        wrap={wrap}
      />
    </div>
  );
}
