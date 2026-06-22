"use client";

import { useCallback, useEffect, useState } from "react";

type FacilityTabletStatus = {
  facilityMode: boolean;
  hasAccount: boolean;
  loading: boolean;
  refresh: () => Promise<void>;
};

export function useFacilityTabletStatus(enabled = true): FacilityTabletStatus {
  const [facilityMode, setFacilityMode] = useState(false);
  const [hasAccount, setHasAccount] = useState(false);
  const [loading, setLoading] = useState(enabled);

  const refresh = useCallback(async () => {
    if (!enabled) {
      setFacilityMode(false);
      setHasAccount(false);
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("/api/facility/status");
      if (!response.ok) {
        setFacilityMode(false);
        setHasAccount(false);
        return;
      }

      const data = (await response.json()) as { hasAccount?: boolean };
      setFacilityMode(true);
      setHasAccount(Boolean(data.hasAccount));
    } catch {
      setFacilityMode(false);
      setHasAccount(false);
    } finally {
      setLoading(false);
    }
  }, [enabled]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return { facilityMode, hasAccount, loading, refresh };
}
