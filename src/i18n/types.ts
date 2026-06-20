export type DeepString<T> = T extends string
  ? string
  : T extends readonly (infer E)[]
    ? readonly DeepString<E>[]
    : T extends object
      ? { [K in keyof T]: DeepString<T[K]> }
      : T;

export type Locale = "en" | "es";

export const LOCALES: Locale[] = ["en", "es"];
export const DEFAULT_LOCALE: Locale = "en";
export const LOCALE_COOKIE = "reentry_locale";

export const LOCALE_LABELS: Record<Locale, string> = {
  en: "English",
  es: "Español",
};
