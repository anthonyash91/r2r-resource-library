"use client";

import { Dropdown, type DropdownOption } from "@/components/ui/dropdown";

export type { DropdownOption as SelectOption };

interface SelectProps {
  label?: string;
  options: DropdownOption[];
  placeholder?: string;
  value?: string;
  onChange?: (e: { target: { value: string; name?: string } }) => void;
  disabled?: boolean;
  className?: string;
  name?: string;
  required?: boolean;
  id?: string;
  searchable?: boolean;
}

/** @deprecated Prefer `Dropdown` directly — this wraps the shared custom dropdown for legacy call sites. */
export function Select({
  label,
  options,
  placeholder,
  value = "",
  onChange,
  disabled,
  className,
  searchable,
}: SelectProps) {
  const mergedOptions =
    placeholder && !options.some((o) => o.value === "")
      ? [{ value: "", label: placeholder }, ...options]
      : options;

  return (
    <Dropdown
      label={label}
      placeholder={placeholder}
      value={value}
      options={mergedOptions}
      onChange={(next) => onChange?.({ target: { value: next } })}
      disabled={disabled}
      className={className}
      searchable={searchable}
    />
  );
}
