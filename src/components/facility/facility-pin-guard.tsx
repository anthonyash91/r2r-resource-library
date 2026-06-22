"use client";

import { useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { wipeTabletLocalState } from "@/lib/facility/tablet-handoff";

export function FacilityPinGuard() {
  const { user, loading } = useAuth();

  useEffect(() => {
    if (loading || !user) return;

    let cancelled = false;

    const verifyBinding = async () => {
      const response = await fetch("/api/facility/verify-login");
      if (cancelled || response.status !== 403) return;

      wipeTabletLocalState();
      await fetch("/api/facility/sign-out", { method: "POST" });
      if (!cancelled) {
        window.location.assign("/");
      }
    };

    void verifyBinding();

    return () => {
      cancelled = true;
    };
  }, [loading, user]);

  return null;
}
