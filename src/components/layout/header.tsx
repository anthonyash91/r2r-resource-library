"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useMemo, useState } from "react";
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
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { LanguageSwitcher } from "@/components/ui/language-switcher";
import { useTranslations } from "@/i18n/locale-context";

export function Header() {
  const pathname = usePathname();
  const { user, isAdmin, signOut, loading } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const { t, locale } = useTranslations();

  const desktopNavClasses =
    locale === "es"
      ? "hidden min-[1720px]:flex"
      : "hidden min-[1400px]:flex";
  const mobileNavClasses =
    locale === "es" ? "min-[1720px]:hidden" : "min-[1400px]:hidden";

  const navLinks = useMemo(
    () => [
      { href: "/resources", label: t("nav.findResources"), icon: Search },
      { href: "/saved", label: t("nav.saved"), icon: Heart },
      { href: "/dashboard", label: t("nav.dashboard"), icon: LayoutDashboard },
      { href: "/faq", label: t("nav.faq"), icon: BookOpen },
    ],
    [t]
  );

  const isActive = (href: string) =>
    pathname === href || (href !== "/" && pathname.startsWith(href));

  const mobileLinkBase =
    "flex min-h-[48px] cursor-pointer items-center gap-3 rounded-xl px-4 py-3 text-base font-medium transition-colors focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring";

  const mobileLinkIcon = "h-5 w-5 shrink-0 text-primary";

  return (
    <header className="sticky top-0 z-50 min-h-[var(--site-header-height)] shrink-0 border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/90">
      <a href="#main-content" className="skip-link">
        {t("common.skipToContent")}
      </a>

      <div className="mx-auto flex min-h-[var(--site-header-height)] max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-3 rounded-lg focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring"
          aria-label={t("nav.homeAriaLabel")}
        >
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <BookOpen className="h-6 w-6" aria-hidden="true" />
          </div>
          <div className="hidden sm:block">
            <span className="block text-lg font-bold leading-tight text-foreground">
              {t("nav.brandName")}
            </span>
            <span className="block text-sm text-muted-foreground">
              {t("nav.tagline")}
            </span>
          </div>
        </Link>

        <nav className={cn("items-center gap-1", desktopNavClasses)} aria-label={t("nav.mainNav")}>
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                "rounded-xl px-4 py-2.5 text-base font-medium transition-colors cursor-pointer",
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

        <div className="flex items-center gap-2">
          <LanguageSwitcher />

          <div className={cn("items-center gap-2", desktopNavClasses)}>
            {!loading && (
              <>
                {user ? (
                  <>
                    {isAdmin && (
                      <Link href="/admin">
                        <Button variant="ghost" size="sm">
                          <Settings className="h-5 w-5" aria-hidden="true" />
                          {t("nav.admin")}
                        </Button>
                      </Link>
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-11 min-h-11 py-2.5"
                      onClick={() => signOut()}
                    >
                      <LogOut className="h-5 w-5" aria-hidden="true" />
                      {t("nav.signOut")}
                    </Button>
                  </>
                ) : (
                  <>
                    <Link href="/login">
                      <Button variant="ghost" size="sm">
                        <LogIn className="h-5 w-5" aria-hidden="true" />
                        {t("nav.signIn")}
                      </Button>
                    </Link>
                    <Link href="/signup">
                      <Button size="sm">{t("nav.createAccount")}</Button>
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
                          signOut();
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
