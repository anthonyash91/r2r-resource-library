"use client";

import { createContext, useContext, useState, type ReactNode } from "react";

interface BreadcrumbContextValue {
  currentLabel: string | null;
  setCurrentLabel: (label: string | null) => void;
}

const BreadcrumbContext = createContext<BreadcrumbContextValue | null>(null);

export function BreadcrumbProvider({ children }: { children: ReactNode }) {
  const [currentLabel, setCurrentLabel] = useState<string | null>(null);

  return (
    <BreadcrumbContext.Provider value={{ currentLabel, setCurrentLabel }}>
      {children}
    </BreadcrumbContext.Provider>
  );
}

export function useBreadcrumbLabel() {
  const context = useContext(BreadcrumbContext);
  if (!context) {
    throw new Error("useBreadcrumbLabel must be used within BreadcrumbProvider");
  }
  return context;
}

export function useBreadcrumbCurrentLabel() {
  const context = useContext(BreadcrumbContext);
  return context?.currentLabel ?? null;
}
