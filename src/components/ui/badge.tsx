import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "primary" | "secondary" | "success" | "warning";
}

export function Badge({ className, variant = "default", children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        variant === "primary" || variant === "secondary" ? "resource-badge" : null,
        variant === "default" && "inline-flex items-center rounded-xl bg-muted px-3 py-1.5 text-sm font-medium text-foreground",
        variant === "success" &&
          "inline-flex items-center rounded-xl bg-success/10 px-3 py-1.5 text-sm font-medium text-success",
        variant === "warning" &&
          "inline-flex items-center rounded-xl bg-warning/10 px-3 py-1.5 text-sm font-medium text-warning",
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
