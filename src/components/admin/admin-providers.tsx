"use client";

import { ConfirmDialogProvider } from "@/components/ui/confirm-dialog";

export function AdminProviders({ children }: { children: React.ReactNode }) {
  return <ConfirmDialogProvider>{children}</ConfirmDialogProvider>;
}
