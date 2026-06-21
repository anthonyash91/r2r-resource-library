export const FAQ_CATEGORIES = [
  { value: "General", labelKey: "faq.general" },
  { value: "Using the Site", labelKey: "faq.usingTheSite" },
  { value: "Accounts & Privacy", labelKey: "faq.accountsAndPrivacy" },
] as const;

export const DEFAULT_FAQ_CATEGORY = FAQ_CATEGORIES[0].value;

export type FaqCategoryValue = (typeof FAQ_CATEGORIES)[number]["value"];

export function faqCategoryLabel(t: (key: string) => string, category: string): string {
  const byValue = FAQ_CATEGORIES.find(
    (item) => item.value.toLowerCase() === category.toLowerCase()
  );
  if (byValue) return t(byValue.labelKey);

  const normalized = category.toLowerCase().replace(/\s+/g, "");
  if (normalized === "general") return t("faq.general");
  if (normalized === "usingthesite") return t("faq.usingTheSite");
  if (normalized === "accounts&privacy" || normalized === "accountsandprivacy") {
    return t("faq.accountsAndPrivacy");
  }

  return category;
}

export function faqCategoryOptions(t: (key: string) => string) {
  return FAQ_CATEGORIES.map(({ value, labelKey }) => ({
    value,
    label: t(labelKey),
  }));
}
