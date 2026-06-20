import type { Metadata } from "next";
import { Source_Sans_3 } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/header";
import { CrisisBar } from "@/components/layout/crisis-bar";
import { Footer } from "@/components/layout/footer";
import { Providers } from "@/components/providers";
import { getServerLocale, getServerTranslator } from "@/i18n/server";

const sourceSans = Source_Sans_3({
  variable: "--font-source-sans",
  subsets: ["latin"],
  weight: ["400", "600", "700"],
});

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: {
      default: t("meta.siteName"),
      template: t("meta.titleTemplate"),
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

  return (
    <html lang={locale} className={`${sourceSans.variable} h-full`}>
      <body className="flex min-h-full flex-col antialiased">
        <Providers initialLocale={locale}>
          <Header />
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
