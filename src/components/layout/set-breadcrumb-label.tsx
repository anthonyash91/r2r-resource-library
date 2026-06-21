"use client";

import { useEffect } from "react";
import { useBreadcrumbLabel } from "@/lib/breadcrumb-context";

export function SetBreadcrumbLabel({ label }: { label: string }) {
  const { setCurrentLabel } = useBreadcrumbLabel();

  useEffect(() => {
    setCurrentLabel(label);
    return () => setCurrentLabel(null);
  }, [label, setCurrentLabel]);

  return null;
}
