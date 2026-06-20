import { cookies } from "next/headers";
import { createTranslator } from "./translator";
import { DEFAULT_LOCALE, LOCALE_COOKIE, type Locale } from "./types";

export async function getServerLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : DEFAULT_LOCALE;
}

export async function getServerTranslator() {
  const locale = await getServerLocale();
  return createTranslator(locale);
}
