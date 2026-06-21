import type { Metadata } from "next";
import { Source_Sans_3 } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/header";
import { BreadcrumbBar } from "@/components/layout/breadcrumb-bar";
import { CrisisBar } from "@/components/layout/crisis-bar";
import { Footer } from "@/components/layout/footer";
import { Providers } from "@/components/providers";
import { getServerLocale, getServerTranslator } from "@/i18n/server";
import { getSiteBranding } from "@/lib/data";

const sourceSans = Source_Sans_3({
  variable: "--font-source-sans",
  subsets: ["latin"],
  weight: ["400", "600", "700"],
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
    <html lang={locale} className={`${sourceSans.variable} h-full`} suppressHydrationWarning>
      <body className="flex min-h-full flex-col antialiased" suppressHydrationWarning>
        <Providers initialLocale={locale}>
          <Header branding={branding} />
          <BreadcrumbBar />
          <main id="main-content" className="flex-1">
            {children}
          </main>
          <CrisisBar />
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
