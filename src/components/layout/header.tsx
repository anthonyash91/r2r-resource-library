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
import {
  HEADER_SHELL_TRANSITION,
  headerCtaClass,
  headerHomeLinkClass,
  headerIconActionClass,
  headerIconButtonClass,
  headerMobileLinkClass,
  headerNavLinkClass,
  headerOutlineActionClass,
  headerTextActionClass,
} from "@/components/layout/header-control-styles";
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/auth-context";
import { LanguageSwitcher } from "@/components/ui/language-switcher";
import { useTranslations } from "@/i18n/locale-context";
import { useFacilityTabletStatus } from "@/hooks/use-facility-tablet-status";
import { useStaffSignInHref } from "@/hooks/use-sign-in-href";
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
  en: "hidden min-[1180px]:flex",
  "es-guest": "hidden min-[1180px]:flex",
  "es-user": "hidden min-[1280px]:flex",
  "es-admin": "hidden min-[1380px]:flex",
};

const MOBILE_NAV_CLASSES: Record<NavLayout, string> = {
  en: "min-[1180px]:hidden",
  "es-guest": "min-[1180px]:hidden",
  "es-user": "min-[1280px]:hidden",
  "es-admin": "min-[1380px]:hidden",
};

import type { SiteBranding } from "@/i18n/localize-content";

const COMPACT_ENTER_Y = 72;
const COMPACT_EXIT_Y = 8;
const FULL_HEADER_HEIGHT = "4.375rem";
const COMPACT_HEADER_HEIGHT = "3.25rem";

interface HeaderProps {
  branding: SiteBranding;
}

export function Header({ branding }: HeaderProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAdmin, signOut, loading, signingOut } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isCompact, setIsCompact] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const isCompactRef = useRef(false);
  const scrollRafRef = useRef<number | null>(null);
  const { t, locale } = useTranslations();
  const shouldFetchFacility = !loading && !user && !signingOut;
  const { facilityMode } = useFacilityTabletStatus(shouldFetchFacility);
  const signInHref = useStaffSignInHref();
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
        "--site-header-offset",
        compact ? COMPACT_HEADER_HEIGHT : FULL_HEADER_HEIGHT
      );
    };

    const updateCompactFromScroll = () => {
      scrollRafRef.current = null;
      const y = window.scrollY;

      setIsScrolled(y > 8);

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
      document.documentElement.style.removeProperty("--site-header-offset");
    };
  }, []);

  const navLinks = useMemo(
    () => [
      { href: "/resources", label: t("nav.findResources"), icon: Search },
      { href: "/#how-it-works", label: t("nav.howItWorks"), icon: BookOpen },
      { href: "/contact", label: t("nav.forCaseWorkers"), icon: BookOpen },
      { href: "/about", label: t("nav.about"), icon: BookOpen },
      ...(user
        ? [
            { href: "/saved", label: t("nav.saved"), icon: Heart },
            { href: "/dashboard", label: t("nav.dashboard"), icon: LayoutDashboard },
          ]
        : []),
    ],
    [t, user]
  );

  const isActive = (href: string) => {
    if (href.startsWith("/#")) {
      return pathname === "/";
    }
    return pathname === href || (href !== "/" && pathname.startsWith(href));
  };

  const mobileLinkIcon = "h-5 w-5 shrink-0 text-primary";

  return (
    <header
      data-compact={isCompact || undefined}
      data-scrolled={isScrolled || undefined}
      className={cn(
        "app-site-header sticky top-0 z-[60] shrink-0 border-b border-border bg-card transition-[box-shadow] duration-300 ease-out",
        HEADER_SHELL_TRANSITION,
        isCompact && "shadow-sm"
      )}
    >
      <a href="#main-content" className="skip-link">
        {t("common.skipToContent")}
      </a>

      <div
        className={cn(
          "app-site-header__inner mx-auto flex w-full max-w-[1280px] items-center justify-between gap-4 px-4 sm:px-9",
          HEADER_SHELL_TRANSITION
        )}
      >
        <Link
          href="/"
          className={headerHomeLinkClass()}
          aria-label={t("nav.homeAriaLabel", { brand: branding.brandName })}
        >
          <HeaderBrandingLockup brandName={branding.brandName} compact={isCompact} />
        </Link>

        <nav
          className={cn(
            "min-w-0 flex-1 flex-nowrap items-center justify-center gap-6 lg:gap-8",
            desktopNavClasses
          )}
          aria-label={t("nav.mainNav")}
        >
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={headerNavLinkClass(isCompact, isActive(href))}
              aria-current={isActive(href) ? "page" : undefined}
            >
              {label}
            </Link>
          ))}
        </nav>

        <div className="flex shrink-0 items-center gap-3 sm:gap-[18px]">
          <LanguageSwitcher compact={isCompact} minimal />

          <div className={cn("shrink-0 items-center gap-3 sm:gap-[18px]", desktopNavClasses)}>
            {!loading && (
              <>
                {user ? (
                  <>
                    {isAdmin && (
                      <Link
                        href="/admin"
                        className={headerIconActionClass(isCompact, isActive("/admin"))}
                        aria-current={isActive("/admin") ? "page" : undefined}
                      >
                        <Settings className="h-4 w-4 shrink-0" aria-hidden="true" />
                        {t("nav.admin")}
                      </Link>
                    )}
                    <button
                      type="button"
                      className={cn(headerOutlineActionClass(isCompact), "gap-1.5")}
                      onClick={handleSignOut}
                      disabled={signingOut}
                      aria-busy={signingOut || undefined}
                    >
                      {signingOut ? (
                        <Loader2 className="h-4 w-4 shrink-0 animate-spin" aria-hidden="true" />
                      ) : (
                        <LogOut className="h-4 w-4 shrink-0" aria-hidden="true" />
                      )}
                      {t("nav.signOut")}
                    </button>
                  </>
                ) : (
                  <>
                    <Link href={signInHref} className={headerTextActionClass(isCompact)}>
                      {t("nav.signIn")}
                    </Link>
                    {showCreateAccount ? (
                      <Link href="/signup" className={headerCtaClass(isCompact)}>
                        {t("nav.getStarted")}
                      </Link>
                    ) : null}
                  </>
                )}
              </>
            )}
          </div>

          <button
            type="button"
            className={cn(headerIconButtonClass(isCompact), mobileNavClasses)}
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-expanded={mobileOpen}
            aria-controls="mobile-menu"
            aria-label={mobileOpen ? t("common.closeMenu") : t("common.openMenu")}
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav
          id="mobile-menu"
          className={cn("border-t border-border bg-card px-4 py-4 sm:px-9", mobileNavClasses)}
          aria-label={t("nav.mobileNav")}
        >
          <ul className="space-y-1">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <li key={href}>
                <Link
                  href={href}
                  className={headerMobileLinkClass(isActive(href))}
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
                          className={headerMobileLinkClass(false)}
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
                          headerMobileLinkClass(false),
                          "w-full",
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
                        className={headerMobileLinkClass(false)}
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
                          headerCtaClass(false),
                          "flex w-full justify-center"
                        )}
                        onClick={() => setMobileOpen(false)}
                      >
                        {t("nav.getStarted")}
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
