"use client";

import { useRouter } from "next/navigation";
import { Search } from "lucide-react";
import { SearchField } from "@/components/ui/search-field";
import { Button } from "@/components/ui/button";
import { useTranslations } from "@/i18n/locale-context";

interface SearchBarProps {
  placeholder?: string;
  size?: "default" | "large";
  variant?: "default" | "hero";
}

export function SearchBar({
  placeholder,
  size = "default",
  variant = "default",
}: SearchBarProps) {
  const router = useRouter();
  const { t } = useTranslations();
  const searchPlaceholder = placeholder ?? t("resources.searchPlaceholder");

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const query = formData.get("q") as string;
    if (query?.trim()) {
      router.push(`/resources?q=${encodeURIComponent(query.trim())}`);
    } else {
      router.push("/resources");
    }
  };

  return (
    <form onSubmit={handleSearch} role="search" aria-label={t("resources.searchAria")}>
      <div className="flex flex-col gap-3 sm:flex-row">
        <div className="flex-1">
          <SearchField
            name="q"
            placeholder={searchPlaceholder}
            iconSize={size === "large" ? "large" : "default"}
            aria-label={t("resources.searchAria")}
          />
        </div>
        <Button
          type="submit"
          size={size === "large" ? "lg" : "md"}
          className={
            variant === "hero"
              ? "bg-card text-primary hover:bg-card/90 sm:min-w-[140px]"
              : "sm:min-w-[140px]"
          }
        >
          <Search className="h-5 w-5" aria-hidden="true" />
          {t("resources.searchButton")}
        </Button>
      </div>
    </form>
  );
}
