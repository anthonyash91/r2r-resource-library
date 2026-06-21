/** Compact tokens for single-page resource layouts */
export const PDF_RESOURCE_PAGE = {
  fontSize: {
    resourceName: 14,
    sectionLabel: 9.5,
    body: 9,
    meta: 8,
    pill: 8,
  },
  spacing: {
    cardPadding: 12,
    cardGap: 10,
    sectionGap: 5,
    titleBodyGap: 8,
    lineGap: 3,
    cardRadius: 8,
    columnGap: 14,
    pillHeight: 20,
    pillPaddingX: 12,
  },
  maxServices: 10,
} as const;

/** PDF design tokens aligned with src/app/globals.css */
export const PDF_THEME = {
  colors: {
    background: "#f9fafb",
    foreground: "#0f172a",
    primary: "#2b4dd0",
    primaryHover: "#2338bd",
    primaryDark: "#1e3a8a",
    primaryMid: "#2b4dd0",
    heroTeal: "#14b8a6",
    brandTagline: "#9ac5f3",
    checkAccent: "#55b4a6",
    secondary: "#eff6ff",
    accent: "#0d9488",
    muted: "#64748b",
    border: "#e2e8f0",
    card: "#ffffff",
    white: "#ffffff",
    success: "#059669",
    badgeBg: "#eff6ff",
    badgeFg: "#2b4dd0",
    badgeBorder: "#d4ddf8",
    eligibilityBg: "#fefce8",
    eligibilityBorder: "#fef08a",
  },
  fontSize: {
    coverTitle: 24,
    coverMeta: 12,
    resourceName: 19,
    sectionLabel: 11,
    body: 12,
    meta: 11,
    pill: 10,
    pageHeader: 11,
    footer: 9,
    coverBrand: 22,
    coverTagline: 12,
    coverDescription: 10,
  },
  spacing: {
    cardPadding: 16,
    cardGap: 20,
    sectionGap: 10,
    lineGap: 4,
    cardRadius: 12,
    accentBarWidth: 6,
  },
} as const;

export type PdfTheme = typeof PDF_THEME;
