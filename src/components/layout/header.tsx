"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useMemo, useState, useEffect, useRef } from "react";
import {
  Menu,
  X,
  BookOpen,
  Search,
  Heart,
  LayoutDashboard,
  LogIn,
  LogOut,
  Loader2,
  Settings,
} from "lucide-react";
import { HeaderBrandingLockup } from "@/components/layout/header-branding-lockup";
import { parseNavTaglinePhrases } from "@/lib/nav-tagline-phrases";
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { LanguageSwitcher } from "@/components/ui/language-switcher";
import { useTranslations } from "@/i18n/locale-context";
import { useFacilityTabletStatus } from "@/hooks/use-facility-tablet-status";
import { useSignInHref } from "@/hooks/use-sign-in-href";
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

const COMPACT_ENTER_Y = 72;
const COMPACT_EXIT_Y = 8;
const FULL_HEADER_HEIGHT = "5rem";
const COMPACT_HEADER_HEIGHT = "3.5rem";

function headerActionClass(isCompact: boolean) {
  return isCompact
    ? "!h-9 !min-h-9 !px-3 !py-1.5 text-sm"
    : "!h-11 !min-h-11 !px-4 !py-2 text-base";
}

interface HeaderProps {
  branding: SiteBranding;
}

export function Header({ branding }: HeaderProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAdmin, signOut, loading, signingOut } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isCompact, setIsCompact] = useState(false);
  const isCompactRef = useRef(false);
  const scrollRafRef = useRef<number | null>(null);
  const { t, locale } = useTranslations();
  const shouldFetchFacility = !loading && !user && !signingOut;
  const { facilityMode } = useFacilityTabletStatus(shouldFetchFacility);
  const signInHref = useSignInHref();
  const showCreateAccount = !facilityMode;

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

  useEffect(() => {
    const applyCompact = (compact: boolean) => {
      if (isCompactRef.current === compact) return;

      isCompactRef.current = compact;
      setIsCompact(compact);
      document.documentElement.style.setProperty(
        "--site-header-height",
        compact ? COMPACT_HEADER_HEIGHT : FULL_HEADER_HEIGHT
      );
    };

    const updateCompactFromScroll = () => {
      scrollRafRef.current = null;
      const y = window.scrollY;

      if (!isCompactRef.current && y >= COMPACT_ENTER_Y) {
        applyCompact(true);
      } else if (isCompactRef.current && y <= COMPACT_EXIT_Y) {
        applyCompact(false);
      }
    };

    const onScroll = () => {
      if (scrollRafRef.current !== null) return;
      scrollRafRef.current = window.requestAnimationFrame(updateCompactFromScroll);
    };

    updateCompactFromScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      if (scrollRafRef.current !== null) {
        window.cancelAnimationFrame(scrollRafRef.current);
      }
      document.documentElement.style.removeProperty("--site-header-height");
    };
  }, []);

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
    <header
      data-compact={isCompact || undefined}
      className={cn(
        "sticky top-0 z-[60] shrink-0 border-b border-border bg-card/95 backdrop-blur transition-[min-height,box-shadow] duration-200 ease-out supports-[backdrop-filter]:bg-card/90",
        isCompact
          ? "min-h-[var(--site-header-height-compact)] shadow-sm"
          : "min-h-[var(--site-header-height)]"
      )}
    >
      <a href="#main-content" className="skip-link">
        {t("common.skipToContent")}
      </a>

      <div
        className={cn(
          "mx-auto flex w-full items-center justify-between gap-3 px-4 transition-[min-height] duration-200 ease-out sm:gap-4 sm:px-6 lg:px-8",
          isCompact
            ? "min-h-[var(--site-header-height-compact)]"
            : "min-h-[var(--site-header-height)]",
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
            compact={isCompact}
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
                "shrink-0 whitespace-nowrap rounded-xl font-medium transition-[padding,font-size] duration-200 ease-out cursor-pointer",
                isCompact ? "px-3 py-1.5 text-sm" : "px-4 py-2.5 text-base",
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
          <LanguageSwitcher compact={isCompact} />

          <div className={cn("shrink-0 items-center gap-2", desktopNavClasses)}>
            {!loading && (
              <>
                {user ? (
                  <>
                    {isAdmin && (
                      <Link
                        href="/admin"
                        className={cn(
                          "inline-flex shrink-0 items-center gap-2 whitespace-nowrap rounded-xl font-medium transition-[padding,height,min-height,font-size] duration-200 ease-out cursor-pointer",
                          headerActionClass(isCompact),
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
                      className={cn(
                        "shrink-0 whitespace-nowrap transition-[height,min-height,padding,font-size] duration-200 ease-out",
                        headerActionClass(isCompact)
                      )}
                      onClick={handleSignOut}
                      loading={signingOut}
                    >
                      <LogOut className="h-5 w-5" aria-hidden="true" />
                      {t("nav.signOut")}
                    </Button>
                  </>
                ) : (
                  <>
                    <Link href={signInHref} className="shrink-0">
                      <Button
                        variant="ghost"
                        size="sm"
                        className={cn("whitespace-nowrap", headerActionClass(isCompact))}
                      >
                        <LogIn className="h-5 w-5" aria-hidden="true" />
                        {t("nav.signIn")}
                      </Button>
                    </Link>
                    {showCreateAccount ? (
                    <Link href="/signup" className="shrink-0">
                      <Button size="sm" className={cn("whitespace-nowrap", headerActionClass(isCompact))}>
                        {t("nav.createAccount")}
                      </Button>
                    </Link>
                    ) : null}
                  </>
                )}
              </>
            )}
          </div>

          <button
            type="button"
            className={cn(
              "flex cursor-pointer items-center justify-center rounded-xl border border-border transition-[width,height] duration-200 ease-out",
              isCompact ? "h-9 w-9" : "h-11 w-11",
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
                          "w-full text-foreground hover:bg-muted",
                          signingOut && "cursor-not-allowed opacity-50"
                        )}
                        onClick={() => {
                          if (signingOut) return;
                          void handleSignOut();
                          setMobileOpen(false);
                        }}
                        disabled={signingOut}
                        aria-busy={signingOut || undefined}
                      >
                        {signingOut ? (
                          <Loader2 className={cn(mobileLinkIcon, "animate-spin")} aria-hidden="true" />
                        ) : (
                          <LogOut className={mobileLinkIcon} aria-hidden="true" />
                        )}
                        {t("nav.signOut")}
                      </button>
                    </li>
                  </>
                ) : (
                  <>
                    <li>
                      <Link
                        href={signInHref}
                        className={cn(mobileLinkBase, "text-foreground hover:bg-muted")}
                        onClick={() => setMobileOpen(false)}
                      >
                        <LogIn className={mobileLinkIcon} aria-hidden="true" />
                        {t("nav.signIn")}
                      </Link>
                    </li>
                    {showCreateAccount ? (
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
                    ) : null}
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
