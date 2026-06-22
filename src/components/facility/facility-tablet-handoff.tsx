"use client";

import { Suspense, useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import {
  stripTabletHandoffParam,
  TABLET_HANDOFF_PARAM,
  wipeTabletLocalState,
} from "@/lib/facility/tablet-handoff";

function FacilityTabletHandoffInner() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (searchParams.get(TABLET_HANDOFF_PARAM) !== "1") return;

    wipeTabletLocalState();

    const nextPath = stripTabletHandoffParam(pathname, searchParams.toString());
    window.location.replace(nextPath);
  }, [pathname, searchParams]);

  return null;
}

export function FacilityTabletHandoff() {
  return (
    <Suspense fallback={null}>
      <FacilityTabletHandoffInner />
    </Suspense>
  );
}
