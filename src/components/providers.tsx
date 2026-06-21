"use client";

import { AuthProvider } from "@/lib/auth-context";
import { SavedProvider } from "@/lib/saved-context";
import { BreadcrumbProvider } from "@/lib/breadcrumb-context";
import { LocaleProvider } from "@/i18n/locale-context";
import type { Locale } from "@/i18n/types";

export function Providers({
  children,
  initialLocale,
}: {
  children: React.ReactNode;
  initialLocale?: Locale;
}) {
  return (
    <LocaleProvider initialLocale={initialLocale}>
      <BreadcrumbProvider>
        <AuthProvider>
          <SavedProvider>{children}</SavedProvider>
        </AuthProvider>
      </BreadcrumbProvider>
    </LocaleProvider>
  );
}
