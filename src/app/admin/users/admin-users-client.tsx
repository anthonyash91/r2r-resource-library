"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import type { Profile } from "@/types";
import { formatDate } from "@/lib/utils";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { useTranslations } from "@/i18n/locale-context";

export function AdminUsersClient({ initialUsers }: { initialUsers: Profile[] }) {
  const { t, locale } = useTranslations();
  const [users, setUsers] = useState(initialUsers);
  const [busyId, setBusyId] = useState<string | null>(null);

  const toggleActive = async (user: Profile) => {
    if (user.is_active && !confirm(t("admin.disableConfirm"))) return;

    const nextActive = !user.is_active;

    if (isSupabaseConfigured()) {
      setBusyId(user.id);
      const supabase = createClient();
      if (supabase) {
        const { error } = await supabase
          .from("profiles")
          .update({ is_active: nextActive })
          .eq("id", user.id);

        setBusyId(null);

        if (error) {
          alert(t("admin.userUpdateFailed"));
          return;
        }
      }
    }

    setUsers((prev) =>
      prev.map((item) => (item.id === user.id ? { ...item, is_active: nextActive } : item))
    );
  };

  const resetPassword = async (email: string) => {
    if (!isSupabaseConfigured()) {
      alert(t("admin.resetPasswordAlert", { email }));
      return;
    }

    const supabase = createClient();
    if (!supabase) return;

    setBusyId(email);
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/login`,
    });
    setBusyId(null);

    if (error) {
      alert(t("admin.userUpdateFailed"));
      return;
    }

    alert(t("admin.resetPasswordSent", { email }));
  };

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.userManagement")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.userManagement")}</p>
      </header>

      <div className="space-y-4">
        {users.map((user) => (
          <Card key={user.id} className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="mb-1 flex flex-wrap gap-2">
                <h2 className="text-lg font-bold">{user.full_name || t("admin.noName")}</h2>
                <Badge variant={user.role === "admin" ? "warning" : "primary"}>{user.role}</Badge>
                <Badge variant={user.is_active ? "success" : "default"}>
                  {user.is_active ? t("common.active") : t("admin.inactive")}
                </Badge>
              </div>
              <p className="text-base text-muted-foreground">{user.email}</p>
              <p className="text-sm text-muted-foreground">
                {formatDate(user.created_at, locale)}
                {user.state && ` · ${user.state}`}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => resetPassword(user.email)}
                disabled={busyId === user.email}
              >
                {t("admin.resetPassword")}
              </Button>
              <Button
                variant={user.is_active ? "ghost" : "primary"}
                size="sm"
                onClick={() => toggleActive(user)}
                disabled={busyId === user.id}
              >
                {user.is_active ? t("admin.disable") : t("admin.enable")}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
