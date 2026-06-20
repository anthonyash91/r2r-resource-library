"use client";

import { forwardRef } from "react";
import { Search } from "lucide-react";
import { cn } from "@/lib/utils";

interface SearchFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  iconSize?: "default" | "large";
}

export const SearchField = forwardRef<HTMLInputElement, SearchFieldProps>(
  ({ className, label, iconSize = "default", id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, "-") || "search";

    return (
      <div className="w-full min-w-0 max-w-full">
        {label && (
          <label htmlFor={inputId} className="mb-2 block text-base font-semibold text-foreground">
            {label}
          </label>
        )}
        <div className="relative">
          <Search
            className={cn(
              "pointer-events-none absolute top-1/2 -translate-y-1/2 text-muted-foreground",
              iconSize === "large" ? "left-5 h-6 w-6" : "left-4 h-5 w-5"
            )}
            aria-hidden="true"
          />
          <input
            ref={ref}
            id={inputId}
            type="search"
            className={cn(
              "w-full min-h-[48px] rounded-xl border-2 border-border bg-card py-3 text-base text-foreground",
              "placeholder:text-muted-foreground",
              "focus:border-primary focus:outline-none focus:ring-2 focus:ring-ring/30",
              iconSize === "large" ? "min-h-[56px] pl-14 text-lg" : "pl-12",
              className
            )}
            {...props}
          />
        </div>
      </div>
    );
  }
);

SearchField.displayName = "SearchField";
