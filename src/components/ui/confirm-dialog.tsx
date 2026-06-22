"use client";

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { useTranslations } from "@/i18n/locale-context";

export interface ConfirmDialogOptions {
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  destructive?: boolean;
}

export interface AlertDialogOptions {
  title: string;
  message: string;
  okLabel?: string;
}

interface DialogContextValue {
  confirm: (options: ConfirmDialogOptions) => Promise<boolean>;
  alert: (options: AlertDialogOptions) => Promise<void>;
}

const DialogContext = createContext<DialogContextValue | null>(null);

type DialogMode = "confirm" | "alert";

interface ActiveDialogState {
  open: boolean;
  mode: DialogMode;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  okLabel?: string;
  destructive?: boolean;
}

const emptyState: ActiveDialogState = {
  open: false,
  mode: "confirm",
  title: "",
  message: "",
};

export function ConfirmDialogProvider({ children }: { children: ReactNode }) {
  const { t } = useTranslations();
  const [state, setState] = useState<ActiveDialogState>(emptyState);
  const confirmResolveRef = useRef<((value: boolean) => void) | null>(null);
  const alertResolveRef = useRef<(() => void) | null>(null);

  const close = useCallback(() => {
    setState(emptyState);
    confirmResolveRef.current = null;
    alertResolveRef.current = null;
  }, []);

  const confirm = useCallback((options: ConfirmDialogOptions) => {
    return new Promise<boolean>((resolve) => {
      confirmResolveRef.current = resolve;
      alertResolveRef.current = null;
      setState({
        open: true,
        mode: "confirm",
        title: options.title,
        message: options.message,
        confirmLabel: options.confirmLabel ?? t("common.confirm"),
        cancelLabel: options.cancelLabel ?? t("common.cancel"),
        destructive: options.destructive ?? false,
      });
    });
  }, [t]);

  const alert = useCallback((options: AlertDialogOptions) => {
    return new Promise<void>((resolve) => {
      alertResolveRef.current = resolve;
      confirmResolveRef.current = null;
      setState({
        open: true,
        mode: "alert",
        title: options.title,
        message: options.message,
        okLabel: options.okLabel ?? t("common.ok"),
      });
    });
  }, [t]);

  const handleCancel = useCallback(() => {
    confirmResolveRef.current?.(false);
    close();
  }, [close]);

  const handleConfirm = useCallback(() => {
    confirmResolveRef.current?.(true);
    close();
  }, [close]);

  const handleOk = useCallback(() => {
    alertResolveRef.current?.();
    close();
  }, [close]);

  const value = useMemo(() => ({ confirm, alert }), [confirm, alert]);

  return (
    <DialogContext.Provider value={value}>
      {children}
      <Modal
        open={state.open}
        onClose={state.mode === "alert" ? handleOk : handleCancel}
        title={state.title}
        closeLabel={state.mode === "alert" ? (state.okLabel ?? t("common.ok")) : (state.cancelLabel ?? t("common.cancel"))}
      >
        <p className="text-base leading-relaxed text-muted-foreground">{state.message}</p>
        <div className="mt-6 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          {state.mode === "confirm" ? (
            <>
              <Button variant="outline" onClick={handleCancel}>
                {state.cancelLabel ?? t("common.cancel")}
              </Button>
              <Button
                variant={state.destructive ? "destructive" : "primary"}
                onClick={handleConfirm}
              >
                {state.confirmLabel ?? t("common.confirm")}
              </Button>
            </>
          ) : (
            <Button variant="primary" onClick={handleOk}>
              {state.okLabel ?? t("common.ok")}
            </Button>
          )}
        </div>
      </Modal>
    </DialogContext.Provider>
  );
}

export function useConfirmDialog(): DialogContextValue {
  const context = useContext(DialogContext);
  if (!context) {
    throw new Error("useConfirmDialog must be used within ConfirmDialogProvider");
  }
  return context;
}
