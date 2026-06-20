import { cn } from "@/lib/utils";
import { forwardRef, type ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", disabled, children, ...props }, ref) => {
    const variants = {
      primary: "bg-primary text-primary-foreground hover:bg-primary-hover",
      secondary: "bg-secondary text-secondary-foreground hover:bg-muted",
      outline: "border-2 border-primary text-primary bg-transparent hover:bg-secondary",
      ghost: "text-primary hover:bg-secondary",
      destructive: "bg-destructive text-white hover:opacity-90",
    };

    const sizes = {
      sm: "min-h-[44px] px-4 py-2 text-base",
      md: "min-h-[48px] px-6 py-3 text-base",
      lg: "min-h-[52px] px-8 py-3.5 text-lg",
    };

    return (
      <button
        ref={ref}
        disabled={disabled}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-xl font-semibold transition-colors cursor-pointer",
          "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
