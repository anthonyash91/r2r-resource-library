"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useMemo, useState, useEffect } from "react";
import {
  Menu,
  X,
  BookOpen,
  Search,
  Heart,
  LayoutDashboard,
  LogIn,
  LogOut,
  Settings,
} from "lucide-react";
import { HeaderBrandingLockup } from "@/components/layout/header-branding-lockup";
import { parseNavTaglinePhrases } from "@/lib/nav-tagline-phrases";
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { LanguageSwitcher } from "@/components/ui/language-switcher";
import { useTranslations } from "@/i18n/locale-context";
import type { Locale } from "@/i18n/types";

type NavLayout = "en" | "es-guest" | "es-user" | "es-admin";

function getNavLayout(locale: Locale, loading: boolean, user: unknown, isAdmin: boolean): NavLayout {
  if (locale !== "es") return "en";
  if (loading) return "es-admin";
  if (user && isAdmin) return "es-admin";
  if (user) return "es-user";
  return "es-guest";
}

const DESKTOP_NAV_CLASSES: Record<NavLayout, string> = {
  en: "hidden min-[1400px]:flex",
  "es-guest": "hidden min-[1180px]:flex",
  "es-user": "hidden min-[1380px]:flex",
  "es-admin": "hidden min-[1540px]:flex",
};

const MOBILE_NAV_CLASSES: Record<NavLayout, string> = {
  en: "min-[1400px]:hidden",
  "es-guest": "min-[1180px]:hidden",
  "es-user": "min-[1380px]:hidden",
  "es-admin": "min-[1540px]:hidden",
};

import type { SiteBranding } from "@/i18n/localize-content";

interface HeaderProps {
  branding: SiteBranding;
}

export function Header({ branding }: HeaderProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAdmin, signOut, loading } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const { t, locale } = useTranslations();

  const handleSignOut = async () => {
    await signOut();
    if (pathname.startsWith("/admin")) {
      router.replace("/login");
      router.refresh();
    }
  };

  const navLayout = getNavLayout(locale, loading, user, isAdmin);
  const desktopNavClasses = DESKTOP_NAV_CLASSES[navLayout];
  const mobileNavClasses = MOBILE_NAV_CLASSES[navLayout];

  useEffect(() => {
    setMobileOpen(false);
  }, [navLayout, locale]);

  const taglinePhrases = useMemo(
    () =>
      parseNavTaglinePhrases(branding.navTagline, [
        t("nav.taglinePhrase1"),
        t("nav.taglinePhrase2"),
        t("nav.taglinePhrase3"),
      ]),
    [branding.navTagline, t]
  );

  const navLinks = useMemo(
    () => [
      { href: "/resources", label: t("nav.findResources"), icon: Search },
      ...(user
        ? [
            { href: "/saved", label: t("nav.saved"), icon: Heart },
            { href: "/dashboard", label: t("nav.dashboard"), icon: LayoutDashboard },
          ]
        : []),
      { href: "/faq", label: t("nav.faqShort"), icon: BookOpen },
    ],
    [t, user]
  );

  const isActive = (href: string) =>
    pathname === href || (href !== "/" && pathname.startsWith(href));

  const mobileLinkBase =
    "flex min-h-[48px] cursor-pointer items-center gap-3 rounded-xl px-4 py-3 text-base font-medium transition-colors focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring";

  const mobileLinkIcon = "h-5 w-5 shrink-0 text-primary";

  return (
    <header className="sticky top-0 z-[60] min-h-[var(--site-header-height)] shrink-0 border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/90">
      <a href="#main-content" className="skip-link">
        {t("common.skipToContent")}
      </a>

      <div
        className={cn(
          "mx-auto flex min-h-[var(--site-header-height)] w-full items-center justify-between gap-3 px-4 sm:gap-4 sm:px-6 lg:px-8",
          locale === "es" ? "max-w-none" : "max-w-7xl"
        )}
      >
        <Link
          href="/"
          className="flex min-w-0 shrink-0 items-center gap-3 rounded-lg focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring"
          aria-label={t("nav.homeAriaLabel", { brand: branding.brandName })}
        >
          <HeaderBrandingLockup
            brandName={branding.brandName}
            taglinePhrases={taglinePhrases}
            textWrapperClassName="hidden min-w-0 sm:flex"
          />
        </Link>

        <nav
          className={cn("shrink-0 flex-nowrap items-center gap-1", desktopNavClasses)}
          aria-label={t("nav.mainNav")}
        >
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                "shrink-0 whitespace-nowrap rounded-xl px-4 py-2.5 text-base font-medium transition-colors cursor-pointer",
                "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring",
                isActive(href)
                  ? "bg-secondary text-primary"
                  : "text-foreground hover:bg-muted"
              )}
              aria-current={isActive(href) ? "page" : undefined}
            >
              {label}
            </Link>
          ))}
        </nav>

        <div className="flex shrink-0 items-center gap-2">
          <LanguageSwitcher />

          <div className={cn("shrink-0 items-center gap-2", desktopNavClasses)}>
            {!loading && (
              <>
                {user ? (
                  <>
                    {isAdmin && (
                      <Link
                        href="/admin"
                        className={cn(
                          "inline-flex h-11 min-h-11 shrink-0 items-center gap-2 whitespace-nowrap rounded-xl px-4 py-2.5 text-base font-medium transition-colors cursor-pointer",
                          "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring",
                          isActive("/admin")
                            ? "bg-secondary text-primary"
                            : "text-foreground hover:bg-muted"
                        )}
                        aria-current={isActive("/admin") ? "page" : undefined}
                      >
                        <Settings className="h-5 w-5 shrink-0" aria-hidden="true" />
                        {t("nav.admin")}
                      </Link>
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-11 min-h-11 shrink-0 whitespace-nowrap py-2.5"
                      onClick={handleSignOut}
                    >
                      <LogOut className="h-5 w-5" aria-hidden="true" />
                      {t("nav.signOut")}
                    </Button>
                  </>
                ) : (
                  <>
                    <Link href="/login" className="shrink-0">
                      <Button variant="ghost" size="sm" className="whitespace-nowrap">
                        <LogIn className="h-5 w-5" aria-hidden="true" />
                        {t("nav.signIn")}
                      </Button>
                    </Link>
                    <Link href="/signup" className="shrink-0">
                      <Button size="sm" className="whitespace-nowrap">
                        {t("nav.createAccount")}
                      </Button>
                    </Link>
                  </>
                )}
              </>
            )}
          </div>

          <button
            type="button"
            className={cn(
              "flex h-11 w-11 cursor-pointer items-center justify-center rounded-xl border border-border",
              mobileNavClasses
            )}
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-expanded={mobileOpen}
            aria-controls="mobile-menu"
            aria-label={mobileOpen ? t("common.closeMenu") : t("common.openMenu")}
          >
            {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav
          id="mobile-menu"
          className={cn("border-t border-border bg-card px-4 py-4", mobileNavClasses)}
          aria-label={t("nav.mobileNav")}
        >
          <ul className="space-y-1">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <li key={href}>
                <Link
                  href={href}
                  className={cn(
                    mobileLinkBase,
                    isActive(href)
                      ? "bg-secondary text-primary"
                      : "text-foreground hover:bg-muted"
                  )}
                  onClick={() => setMobileOpen(false)}
                  aria-current={isActive(href) ? "page" : undefined}
                >
                  <Icon className={mobileLinkIcon} aria-hidden="true" />
                  {label}
                </Link>
              </li>
            ))}
            {!loading && (
              <>
                {user ? (
                  <>
                    {isAdmin && (
                      <li>
                        <Link
                          href="/admin"
                          className={cn(mobileLinkBase, "text-foreground hover:bg-muted")}
                          onClick={() => setMobileOpen(false)}
                        >
                          <Settings className={mobileLinkIcon} aria-hidden="true" />
                          {t("nav.adminPortal")}
                        </Link>
                      </li>
                    )}
                    <li>
                      <button
                        type="button"
                        className={cn(
                          mobileLinkBase,
                          "w-full text-foreground hover:bg-muted"
                        )}
                        onClick={() => {
                          void handleSignOut();
                          setMobileOpen(false);
                        }}
                      >
                        <LogOut className={mobileLinkIcon} aria-hidden="true" />
                        {t("nav.signOut")}
                      </button>
                    </li>
                  </>
                ) : (
                  <>
                    <li>
                      <Link
                        href="/login"
                        className={cn(mobileLinkBase, "text-foreground hover:bg-muted")}
                        onClick={() => setMobileOpen(false)}
                      >
                        <LogIn className={mobileLinkIcon} aria-hidden="true" />
                        {t("nav.signIn")}
                      </Link>
                    </li>
                    <li>
                      <Link
                        href="/signup"
                        className={cn(
                          mobileLinkBase,
                          "bg-primary font-semibold text-primary-foreground hover:bg-primary-hover"
                        )}
                        onClick={() => setMobileOpen(false)}
                      >
                        {t("nav.createAccount")}
                      </Link>
                    </li>
                  </>
                )}
              </>
            )}
          </ul>
        </nav>
      )}
    </header>
  );
}
