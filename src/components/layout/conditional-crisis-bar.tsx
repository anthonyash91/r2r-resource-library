"use client";

import { usePathname } from "next/navigation";
import { CrisisBar } from "@/components/layout/crisis-bar";

/** Crisis line also appears in the promo bar on the homepage. */
export function ConditionalCrisisBar() {
  const pathname = usePathname();
  if (pathname === "/") return null;
  return <CrisisBar />;
}
