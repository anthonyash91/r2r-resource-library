"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useTransition } from "react";
import type { Category } from "@/types";
import { CategoryIcon } from "@/lib/category-icons";
import { Dropdown } from "@/components/ui/dropdown";
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

function useCategoryLabel() {
  const { t } = useTranslations();

  return (category: Category) => {
    const key = `categories.${category.slug}.name`;
    const translated = t(key);
    return translated === key ? category.name : translated;
  };
}

function CategorySelect({
  categories,
  activeSlug,
  onChange,
  hideLabel = false,
}: {
  categories: Category[];
  activeSlug: string | null;
  onChange: (slug: string) => void;
  hideLabel?: boolean;
}) {
  const { t } = useTranslations();
  const categoryLabel = useCategoryLabel();

  const options = [
    { value: "", label: t("common.all") },
    ...categories.map((category) => ({
      value: category.slug,
      label: categoryLabel(category),
    })),
  ];

  return (
    <Dropdown
      label={hideLabel ? undefined : t("resources.browseByCategory")}
      hideLabel={hideLabel}
      placeholder={t("resources.allCategories")}
      value={activeSlug ?? ""}
      onChange={onChange}
      options={options}
      searchPlaceholder={t("resources.searchCategories")}
    />
  );
}

function CategoryPillsList({
  categories,
  compact,
  activeSlug,
  buildHref,
  onCategoryChange,
  wrap = false,
}: {
  categories: Category[];
  compact: boolean;
  activeSlug: string | null;
  buildHref: (slug?: string) => string;
  onCategoryChange: (slug: string) => void;
  wrap?: boolean;
}) {
  const { t } = useTranslations();
  const categoryLabel = useCategoryLabel();

  return (
    <div className={cn("w-full min-w-0", !compact && "mb-0")}>
      {!compact && (
        <p className="mb-2 hidden text-sm font-medium text-muted-foreground md:block">
          {t("resources.browseByCategory")}
        </p>
      )}

      <div className="md:hidden w-full min-w-0 rounded-2xl border border-border bg-card px-4 pb-5 pt-4 sm:px-5">
        <CategorySelect
          categories={categories}
          activeSlug={activeSlug}
          onChange={onCategoryChange}
          hideLabel={compact}
        />
      </div>

      <div
        className={cn(
          "hidden gap-2 md:flex",
          wrap ? "flex-wrap justify-center" : "overflow-x-auto pb-1"
        )}
        role="list"
        aria-label={t("resources.browseByCategory")}
      >
        <PillLink href={buildHref()} isActive={!activeSlug}>
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
  const router = useRouter();
  const searchParams = useSearchParams();
  const [, startTransition] = useTransition();
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

  const onCategoryChange = (slug: string) => {
    startTransition(() => {
      router.push(buildHref(slug || undefined));
    });
  };

  return (
    <div className={className}>
      <CategoryPillsList
        categories={categories}
        compact={compact ?? false}
        activeSlug={activeSlug}
        buildHref={buildHref}
        onCategoryChange={onCategoryChange}
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
  const router = useRouter();
  const [, startTransition] = useTransition();

  const buildHref = (slug?: string) =>
    slug ? `/resources?category=${slug}` : "/resources";

  const onCategoryChange = (slug: string) => {
    startTransition(() => {
      router.push(buildHref(slug || undefined));
    });
  };

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

  return (
    <div className={className}>
      <CategoryPillsList
        categories={categories}
        compact={compact}
        activeSlug={activeSlug}
        buildHref={buildHref}
        onCategoryChange={onCategoryChange}
        wrap={wrap}
      />
    </div>
  );
}
