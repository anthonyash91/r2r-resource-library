"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { createTranslator, type Translator } from "./translator";
import { DEFAULT_LOCALE, LOCALE_COOKIE, LOCALE_LABELS, type Locale } from "./types";

interface LocaleContextValue extends Translator {
  setLocale: (locale: Locale) => void;
}

const LocaleContext = createContext<LocaleContextValue | null>(null);

function readCookieLocale(): Locale {
  if (typeof document === "undefined") return DEFAULT_LOCALE;
  const match = document.cookie.match(new RegExp(`(?:^|; )${LOCALE_COOKIE}=([^;]*)`));
  return match?.[1] === "es" ? "es" : DEFAULT_LOCALE;
}

function writeCookieLocale(locale: Locale) {
  document.cookie = `${LOCALE_COOKIE}=${locale};path=/;max-age=31536000;samesite=lax`;
}

export function LocaleProvider({
  children,
  initialLocale = DEFAULT_LOCALE,
}: {
  children: ReactNode;
  initialLocale?: Locale;
}) {
  const router = useRouter();
  const [locale, setLocaleState] = useState<Locale>(initialLocale);

  useEffect(() => {
    const cookieLocale = readCookieLocale();
    if (cookieLocale !== locale) {
      setLocaleState(cookieLocale);
    }
  }, [locale]);

  const setLocale = useCallback(
    (nextLocale: Locale) => {
      writeCookieLocale(nextLocale);
      setLocaleState(nextLocale);
      router.refresh();
    },
    [router]
  );

  const value = useMemo(() => {
    const translator = createTranslator(locale);
    return { ...translator, setLocale };
  }, [locale, setLocale]);

  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const context = useContext(LocaleContext);
  if (!context) {
    throw new Error("useLocale must be used within LocaleProvider");
  }
  return context;
}

export function useTranslations() {
  const { t, locale, messages, setLocale } = useLocale();
  return { t, locale, messages, setLocale, labels: LOCALE_LABELS };
}
