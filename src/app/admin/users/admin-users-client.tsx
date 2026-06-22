"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Modal } from "@/components/ui/modal";
import type { AdminUserListItem } from "@/types";
import { formatDate } from "@/lib/utils";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { useAuth } from "@/lib/auth-context";
import { isFacilityAuthEmail } from "@/lib/facility/auth-email";
import { useTranslations } from "@/i18n/locale-context";
import { useConfirmDialog } from "@/components/ui/confirm-dialog";

function displayEmail(user: AdminUserListItem): string {
  if (user.contact_email?.trim()) return user.contact_email.trim();
  if (user.signup_context === "facility" && isFacilityAuthEmail(user.email)) {
    return "";
  }
  return user.email;
}

export function AdminUsersClient({ initialUsers }: { initialUsers: AdminUserListItem[] }) {
  const { t, locale } = useTranslations();
  const { user: currentUser } = useAuth();
  const { confirm, alert } = useConfirmDialog();
  const [users, setUsers] = useState(initialUsers);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [facilityResetUser, setFacilityResetUser] = useState<AdminUserListItem | null>(null);
  const [newPin, setNewPin] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [resetPinError, setResetPinError] = useState("");

  const toggleActive = async (user: AdminUserListItem) => {
    if (user.is_active) {
      const confirmed = await confirm({
        title: t("admin.disable"),
        message: t("admin.disableConfirm"),
        confirmLabel: t("admin.disable"),
        destructive: true,
      });
      if (!confirmed) return;
    }

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
          await alert({ title: t("common.error"), message: t("admin.userUpdateFailed") });
          return;
        }
      }
    }

    setUsers((prev) =>
      prev.map((item) => (item.id === user.id ? { ...item, is_active: nextActive } : item))
    );
  };

  const resetPassword = async (email: string) => {
    if (!email) {
      await alert({ title: t("common.error"), message: t("admin.resetPasswordUnavailable") });
      return;
    }

    const confirmed = await confirm({
      title: t("admin.resetPassword"),
      message: t("admin.resetPasswordConfirm", { email }),
      confirmLabel: t("admin.resetPassword"),
    });
    if (!confirmed) return;

    if (!isSupabaseConfigured()) {
      await alert({ title: t("common.notice"), message: t("admin.resetPasswordAlert", { email }) });
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
      await alert({ title: t("common.error"), message: t("admin.userUpdateFailed") });
      return;
    }

    await alert({ title: t("common.success"), message: t("admin.resetPasswordSent", { email }) });
  };

  const openFacilityPinReset = (user: AdminUserListItem) => {
    setFacilityResetUser(user);
    setNewPin("");
    setNewPassword("");
    setResetPinError("");
  };

  const closeFacilityPinReset = () => {
    if (busyId) return;
    setFacilityResetUser(null);
    setNewPin("");
    setNewPassword("");
    setResetPinError("");
  };

  const submitFacilityPinReset = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!facilityResetUser) return;

    const pin = newPin.trim();
    if (!pin || newPassword.length < 8) {
      setResetPinError(t("admin.resetPinInvalid"));
      return;
    }

    setResetPinError("");
    setBusyId(facilityResetUser.id);

    const response = await fetch(`/api/admin/users/${facilityResetUser.id}/reset-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pin, password: newPassword }),
    });

    setBusyId(null);

    if (!response.ok) {
      const payload = (await response.json().catch(() => ({}))) as { error?: string };
      setResetPinError(payload.error ?? t("admin.resetPinFailed"));
      return;
    }

    setFacilityResetUser(null);
    setNewPin("");
    setNewPassword("");
    await alert({ title: t("common.success"), message: t("admin.resetPinSuccess") });
  };

  const deleteUser = async (user: AdminUserListItem) => {
    if (user.id === currentUser?.id) {
      await alert({ title: t("common.error"), message: t("admin.cannotDeleteSelf") });
      return;
    }

    if (user.role === "admin") {
      await alert({ title: t("common.error"), message: t("admin.cannotDeleteAdmin") });
      return;
    }

    const displayName = user.full_name || displayEmail(user) || t("admin.noName");
    const confirmed = await confirm({
      title: t("admin.deleteUser"),
      message: t("admin.deleteUserConfirm", { name: displayName }),
      confirmLabel: t("admin.deleteUser"),
      destructive: true,
    });
    if (!confirmed) return;

    setBusyId(user.id);
    const response = await fetch(`/api/admin/users/${user.id}`, { method: "DELETE" });
    setBusyId(null);

    if (!response.ok) {
      const payload = (await response.json().catch(() => ({}))) as { error?: string };
      await alert({
        title: t("common.error"),
        message: payload.error ?? t("admin.deleteUserFailed"),
      });
      return;
    }

    setUsers((prev) => prev.filter((item) => item.id !== user.id));
    await alert({ title: t("common.success"), message: t("admin.deleteUserSuccess") });
  };

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.userManagement")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.userManagementDesc")}</p>
      </header>

      <div className="space-y-4">
        {users.map((user) => {
          const email = displayEmail(user);
          const isFacilityUser = user.signup_context === "facility";
          const isSelf = user.id === currentUser?.id;
          const canDelete = user.role !== "admin" && !isSelf;

          return (
            <Card key={user.id} className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <div className="mb-1 flex flex-wrap gap-2">
                  <h2 className="text-lg font-bold">{user.full_name || t("admin.noName")}</h2>
                  <Badge variant={user.role === "admin" ? "warning" : "primary"}>{user.role}</Badge>
                  <Badge variant={user.is_active ? "success" : "default"}>
                    {user.is_active ? t("common.active") : t("admin.inactive")}
                  </Badge>
                </div>
                {user.signup_context === "facility" ? (
                  <p className="text-base text-muted-foreground">
                    {user.facility_name
                      ? t("admin.userFacility", { name: user.facility_name })
                      : t("admin.userFacilityUnknown")}
                  </p>
                ) : null}
                {email ? <p className="text-base text-muted-foreground">{email}</p> : null}
                {user.signup_context === "facility" && !email ? (
                  <p className="text-base text-muted-foreground">{t("admin.facilityAccountNoEmail")}</p>
                ) : null}
                <p className="text-sm text-muted-foreground">
                  {formatDate(user.created_at, locale)}
                  {user.state && ` · ${user.state}`}
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                {isFacilityUser ? (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => openFacilityPinReset(user)}
                    loading={busyId === user.id}
                  >
                    {t("admin.resetPin")}
                  </Button>
                ) : email ? (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => resetPassword(email)}
                    loading={busyId === user.email}
                  >
                    {t("admin.resetPassword")}
                  </Button>
                ) : null}
                <Button
                  variant={user.is_active ? "ghost" : "primary"}
                  size="sm"
                  onClick={() => toggleActive(user)}
                  loading={busyId === user.id}
                >
                  {user.is_active ? t("admin.disable") : t("admin.enable")}
                </Button>
                {canDelete ? (
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-destructive hover:text-destructive"
                    onClick={() => deleteUser(user)}
                    loading={busyId === user.id}
                  >
                    {t("admin.deleteUser")}
                  </Button>
                ) : null}
              </div>
            </Card>
          );
        })}
      </div>

      <Modal
        open={facilityResetUser !== null}
        onClose={closeFacilityPinReset}
        title={t("admin.resetPinTitle")}
        closeLabel={t("common.cancel")}
        disableClose={busyId === facilityResetUser?.id}
      >
        <form onSubmit={submitFacilityPinReset}>
          <p className="mb-4 text-base leading-relaxed text-muted-foreground">
            {t("admin.resetPinDesc")}
          </p>
          <div className="space-y-4">
            <Input
              label={t("admin.resetPinPinLabel")}
              value={newPin}
              onChange={(e) => setNewPin(e.target.value)}
              autoComplete="off"
              required
            />
            <Input
              label={t("admin.resetPinPasswordLabel")}
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              hint={t("admin.resetPinPasswordHint")}
              autoComplete="new-password"
              minLength={8}
              required
            />
            {resetPinError ? (
              <p role="alert" className="text-sm text-destructive">
                {resetPinError}
              </p>
            ) : null}
          </div>
          <div className="mt-6 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
            <Button
              type="button"
              variant="outline"
              onClick={closeFacilityPinReset}
              disabled={busyId === facilityResetUser?.id}
            >
              {t("common.cancel")}
            </Button>
            <Button type="submit" loading={busyId === facilityResetUser?.id}>
              {t("admin.resetPin")}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
