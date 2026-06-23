"use client";

import { useAuth } from "@/lib/auth-context";
import { useFacilityTabletStatus } from "@/hooks/use-facility-tablet-status";

/**
 * Sign-in href for general (staff/public) entry — always the email login page.
 * Inmates on facility tablets should use /facility/login via the session banner.
 */
export function useStaffSignInHref(): string {
  return "/login";
}

export function useSignInHref(): string {
  const { user, loading } = useAuth();
  const { facilityMode } = useFacilityTabletStatus(!loading && !user);
  return facilityMode ? "/facility/login" : "/login";
}
