"use client";

import { useCallback, useEffect, useRef } from "react";
import { useAuth } from "@/lib/auth-context";
import { FACILITY_INACTIVITY_MS } from "@/lib/facility/inactivity";

const ACTIVITY_EVENTS = ["mousedown", "keydown", "touchstart", "scroll"] as const;

export function FacilityInactivityGuard({ children }: { children: React.ReactNode }) {
  const { signOut, user } = useAuth();
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const facilityModeRef = useRef(false);

  const clearTimer = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, []);

  const scheduleSignOut = useCallback(() => {
    clearTimer();
    if (!facilityModeRef.current || !user) return;

    timeoutRef.current = setTimeout(() => {
      void signOut();
    }, FACILITY_INACTIVITY_MS);
  }, [clearTimer, signOut, user]);

  useEffect(() => {
    let cancelled = false;

    fetch("/api/facility/status")
      .then((res) => {
        if (!cancelled) {
          facilityModeRef.current = res.ok;
          scheduleSignOut();
        }
      })
      .catch(() => {
        facilityModeRef.current = false;
      });

    return () => {
      cancelled = true;
    };
  }, [scheduleSignOut, user]);

  useEffect(() => {
    if (!user) {
      clearTimer();
      return;
    }

    const onActivity = () => scheduleSignOut();

    ACTIVITY_EVENTS.forEach((event) => {
      window.addEventListener(event, onActivity, { passive: true });
    });

    scheduleSignOut();

    return () => {
      clearTimer();
      ACTIVITY_EVENTS.forEach((event) => {
        window.removeEventListener(event, onActivity);
      });
    };
  }, [clearTimer, scheduleSignOut, user]);

  return <>{children}</>;
}
