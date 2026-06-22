"use client";

import { useAuth } from "@/lib/auth-context";
import { useFacilityTabletStatus } from "@/hooks/use-facility-tablet-status";

export function useSignInHref(): string {
  const { user, loading } = useAuth();
  const { facilityMode } = useFacilityTabletStatus(!loading && !user);
  return facilityMode ? "/facility/login" : "/login";
}
