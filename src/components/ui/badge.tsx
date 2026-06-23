import { cn } from "@/lib/utils";
import type { LucideIcon } from "lucide-react";
import type { HTMLAttributes } from "react";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "primary" | "secondary" | "success" | "warning";
  icon?: LucideIcon;
}

export function Badge({
  className,
  variant = "default",
  icon: Icon,
  children,
  ...props
}: BadgeProps) {
  return (
    <span
      className={cn(
        variant === "primary" || variant === "secondary" ? "resource-badge" : null,
        variant === "default" &&
          "inline-flex items-center gap-1.5 rounded-xl border border-border bg-muted px-3 py-1.5 text-sm font-medium text-foreground",
        variant === "success" &&
          "inline-flex items-center gap-1.5 rounded-xl border border-success/15 bg-success/10 px-3 py-1.5 text-sm font-medium text-success",
        variant === "warning" &&
          "inline-flex items-center gap-1.5 rounded-xl border border-warning/15 bg-warning/10 px-3 py-1.5 text-sm font-medium text-warning",
        className
      )}
      {...props}
    >
      {Icon ? <Icon className="h-3.5 w-3.5 shrink-0" aria-hidden="true" /> : null}
      {children}
    </span>
  );
}
