import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";
import { forwardRef, type ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?:
    | "primary"
    | "secondary"
    | "outline"
    | "ghost"
    | "destructive"
    | "soft"
    | "soft-primary"
    | "soft-accent"
    | "soft-success"
    | "soft-warning"
    | "soft-destructive";
  size?: "sm" | "md" | "lg" | "badge";
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { className, variant = "primary", size = "md", disabled, loading = false, children, ...props },
    ref
  ) => {
    const variants = {
      primary: "bg-primary text-primary-foreground hover:bg-primary-hover",
      secondary: "bg-secondary text-secondary-foreground hover:bg-muted",
      outline: "border-2 border-primary text-primary bg-transparent hover:bg-secondary",
      ghost: "text-primary hover:bg-secondary",
      destructive: "bg-destructive text-white hover:opacity-90",
      soft: "border border-transparent bg-muted font-medium text-foreground hover:bg-muted/80",
      "soft-primary":
        "border border-primary/15 bg-primary/10 font-medium text-primary hover:bg-primary/15",
      "soft-accent":
        "border border-accent/15 bg-accent/10 font-medium text-accent hover:bg-accent/15",
      "soft-success":
        "border border-success/15 bg-success/10 font-medium text-success hover:bg-success/15",
      "soft-warning":
        "border border-warning/15 bg-warning/10 font-medium text-warning hover:bg-warning/15",
      "soft-destructive":
        "border border-destructive/15 bg-destructive/10 font-medium text-destructive hover:bg-destructive/15",
    };

    const sizes = {
      badge: "min-h-0 h-auto gap-1.5 px-3 py-1.5 text-sm",
      sm: "min-h-[44px] px-4 py-2 text-base",
      md: "min-h-[48px] px-6 py-3 text-base",
      lg: "min-h-[52px] px-8 py-3.5 text-lg",
    };

    const isSoft = variant.startsWith("soft");

    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        aria-busy={loading || undefined}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-xl transition-colors cursor-pointer",
          isSoft ? "font-medium" : "font-semibold",
          "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {loading ? <Loader2 className="h-4 w-4 shrink-0 animate-spin" aria-hidden="true" /> : null}
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
