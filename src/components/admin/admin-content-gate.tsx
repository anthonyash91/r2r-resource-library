"use client";

import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";

export function AdminContentGate({ children }: { children: React.ReactNode }) {
  const { user, isAdmin, loading } = useAuth();
  const { t } = useTranslations();

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <p className="text-lg text-muted-foreground">{t("common.loading")}</p>
      </div>
    );
  }

  if (!user || !isAdmin) {
    return null;
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="p-4 sm:p-6 lg:p-8">{children}</div>
    </div>
  );
}
