import type { Metadata } from "next";
import { DM_Sans, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/header";
import { BreadcrumbBar } from "@/components/layout/breadcrumb-bar";
import { ConditionalCrisisBar } from "@/components/layout/conditional-crisis-bar";
import { Footer } from "@/components/layout/footer";
import { PromoBar } from "@/components/layout/promo-bar";
import { Providers } from "@/components/providers";
import { TopSessionBanner } from "@/components/layout/top-session-banner";
import { getServerLocale, getServerTranslator } from "@/i18n/server";
import { getSiteBranding } from "@/lib/data";

const plusJakarta = Plus_Jakarta_Sans({
  variable: "--font-plus-jakarta",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  const branding = await getSiteBranding();

  return {
    title: {
      default: branding.brandName,
      template: `%s | ${branding.brandName}`,
    },
    description: t("meta.description"),
  };
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await getServerLocale();
  const branding = await getSiteBranding();

  return (
    <html
      lang={locale}
      className={`${plusJakarta.variable} ${dmSans.variable} h-full`}
      suppressHydrationWarning
    >
      <body className="flex min-h-full flex-col antialiased" suppressHydrationWarning>
        <Providers initialLocale={locale}>
          <PromoBar />
          <Header branding={branding} />
          <TopSessionBanner />
          <BreadcrumbBar />
          <main id="main-content" className="flex-1">
            {children}
          </main>
          <ConditionalCrisisBar />
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
