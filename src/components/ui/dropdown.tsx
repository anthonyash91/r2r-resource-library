"use client";

import { useEffect, useId, useMemo, useRef, useState } from "react";
import { ChevronDown, Check, Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";

export interface DropdownOption {
  value: string;
  label: string;
}

interface DropdownProps {
  label?: string;
  placeholder?: string;
  value: string;
  options: DropdownOption[];
  onChange: (value: string) => void;
  disabled?: boolean;
  searchable?: boolean;
  searchPlaceholder?: string;
  noResultsText?: string;
  className?: string;
  hideLabel?: boolean;
}

export function Dropdown({
  label,
  placeholder,
  value,
  options,
  onChange,
  disabled = false,
  searchable,
  searchPlaceholder,
  noResultsText,
  className,
  hideLabel = false,
}: DropdownProps) {
  const { t } = useTranslations();
  const resolvedPlaceholder = placeholder ?? t("common.default");
  const resolvedSearchPlaceholder = searchPlaceholder ?? t("common.search");
  const resolvedNoResults = noResultsText ?? t("resources.noResults");

  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [highlightIndex, setHighlightIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);
  const listboxId = useId();
  const labelId = useId();
  const searchId = useId();

  const isSearchable = searchable ?? options.length > 4;

  const selected = options.find((opt) => opt.value === value);
  const displayLabel = selected?.label ?? resolvedPlaceholder;

  const filteredOptions = useMemo(() => {
    if (!isSearchable || !searchQuery.trim()) return options;

    const query = searchQuery.trim().toLowerCase();
    return options.filter((option) => {
      if (option.value === "") return true;
      return option.label.toLowerCase().includes(query);
    });
  }, [options, searchQuery, isSearchable]);

  const closeDropdown = () => {
    setOpen(false);
    setSearchQuery("");
    setHighlightIndex(-1);
  };

  useEffect(() => {
    if (!open) return;

    const handleClickOutside = (e: MouseEvent) => {
      if (!containerRef.current?.contains(e.target as Node)) {
        closeDropdown();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  useEffect(() => {
    if (open && isSearchable) {
      requestAnimationFrame(() => searchRef.current?.focus());
    }
  }, [open, isSearchable]);

  useEffect(() => {
    if (!open) return;
    const selectedIndex = filteredOptions.findIndex((o) => o.value === value);
    setHighlightIndex(selectedIndex >= 0 ? selectedIndex : 0);
  }, [open, searchQuery, filteredOptions, value]);

  const selectOption = (optionValue: string) => {
    onChange(optionValue);
    closeDropdown();
  };

  const openDropdown = () => {
    if (disabled) return;
    setOpen(true);
  };

  const handleTriggerKeyDown = (e: React.KeyboardEvent) => {
    if (disabled) return;

    if (e.key === "Escape") {
      closeDropdown();
      return;
    }

    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      if (!open) {
        openDropdown();
        return;
      }
      if (highlightIndex >= 0 && highlightIndex < filteredOptions.length) {
        selectOption(filteredOptions[highlightIndex].value);
      }
      return;
    }

    if (!open && (e.key === "ArrowDown" || e.key === "ArrowUp")) {
      e.preventDefault();
      openDropdown();
    }
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Escape") {
      e.stopPropagation();
      closeDropdown();
      return;
    }

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlightIndex((i) => Math.min(i + 1, filteredOptions.length - 1));
      return;
    }

    if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightIndex((i) => Math.max(i - 1, 0));
      return;
    }

    if (e.key === "Enter") {
      e.preventDefault();
      if (highlightIndex >= 0 && highlightIndex < filteredOptions.length) {
        selectOption(filteredOptions[highlightIndex].value);
      }
    }
  };

  const searchAriaLabel = label
    ? `${t("common.search")} ${label}`
    : resolvedSearchPlaceholder;

  return (
    <div ref={containerRef} className={cn("relative w-full", className)}>
      {label && (
        <span
          id={labelId}
          className={cn(
            "mb-2 block text-base font-semibold text-foreground",
            hideLabel && "sr-only"
          )}
        >
          {label}
        </span>
      )}

      <button
        type="button"
        disabled={disabled}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-labelledby={label ? labelId : undefined}
        aria-controls={listboxId}
        onClick={() => (open ? closeDropdown() : openDropdown())}
        onKeyDown={handleTriggerKeyDown}
        className={cn(
          "flex w-full min-h-[48px] cursor-pointer items-center justify-between gap-3 rounded-xl border-2 border-border bg-card px-4 py-3 text-left text-base transition-colors",
          "focus:border-primary focus:outline-none focus:ring-2 focus:ring-ring/30",
          disabled && "cursor-not-allowed opacity-50",
          !selected && "text-muted-foreground"
        )}
      >
        <span className="truncate">{displayLabel}</span>
        <ChevronDown
          className={cn("h-5 w-5 shrink-0 text-muted-foreground transition-transform", open && "rotate-180")}
          aria-hidden="true"
        />
      </button>

      {open && (
        <div className="absolute z-50 mt-2 w-full overflow-hidden rounded-xl border border-border bg-card shadow-lg">
          {isSearchable && (
            <div className="sticky top-0 border-b border-border bg-card p-2">
              <div className="relative">
                <Search
                  className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
                  aria-hidden="true"
                />
                <input
                  ref={searchRef}
                  id={searchId}
                  type="search"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={handleSearchKeyDown}
                  placeholder={resolvedSearchPlaceholder}
                  aria-controls={listboxId}
                  aria-label={searchAriaLabel}
                  className="w-full min-h-[40px] rounded-lg border border-border bg-background py-2 pl-9 pr-3 text-base text-foreground placeholder:text-muted-foreground focus:border-transparent focus:outline-none focus:ring-0 focus-visible:outline-none"
                />
              </div>
            </div>
          )}

          <ul
            id={listboxId}
            role="listbox"
            aria-label={label ?? resolvedPlaceholder}
            className="max-h-60 overflow-auto py-1"
          >
            {filteredOptions.length === 0 ? (
              <li className="px-4 py-3 text-base text-muted-foreground">{resolvedNoResults}</li>
            ) : (
              filteredOptions.map((option, index) => {
                const isSelected = option.value === value;
                const isHighlighted = index === highlightIndex;

                return (
                  <li
                    key={option.value || `placeholder-${option.label}`}
                    role="option"
                    aria-selected={isSelected}
                    onMouseEnter={() => setHighlightIndex(index)}
                    onClick={() => selectOption(option.value)}
                    className={cn(
                      "flex cursor-pointer items-center justify-between gap-2 px-4 py-3 text-base",
                      (isSelected || isHighlighted) && "bg-secondary text-primary",
                      !isSelected && !isHighlighted && "text-foreground hover:bg-muted"
                    )}
                  >
                    <span className="truncate">{option.label}</span>
                    {isSelected && <Check className="h-4 w-4 shrink-0" aria-hidden="true" />}
                  </li>
                );
              })
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
