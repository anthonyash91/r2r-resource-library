"use client";

import { useTranslations } from "@/i18n/locale-context";
import { cn } from "@/lib/utils";

type LibraryDisclaimerVariant = "footer" | "detail";

interface LibraryDisclaimerProps {
  variant: LibraryDisclaimerVariant;
  className?: string;
}

const copyKeys: Record<LibraryDisclaimerVariant, "libraryDisclaimer.footer" | "libraryDisclaimer.detail"> = {
  footer: "libraryDisclaimer.footer",
  detail: "libraryDisclaimer.detail",
};

export function LibraryDisclaimer({ variant, className }: LibraryDisclaimerProps) {
  const { t } = useTranslations();

  if (variant === "detail") {
    return (
      <aside
        role="note"
        className={cn("app-library-disclaimer-bar border-t border-border", className)}
      >
        <div className="mx-auto max-w-7xl px-4 py-3 sm:px-6 lg:px-8">
          <p className="text-center text-sm leading-relaxed">
            {t(copyKeys.detail)}
          </p>
        </div>
      </aside>
    );
  }

  return (
    <p
      role="note"
      className={cn("text-sm leading-relaxed text-[var(--footer-muted)]", className)}
    >
      {t(copyKeys.footer)}
    </p>
  );
}
