"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  FolderOpen,
  Tags,
  Users,
  FileText,
  Megaphone,
  HelpCircle,
  Home,
  Building2,
  LogOut,
  Menu,
  X,
} from "lucide-react";
import { useMemo, useState } from "react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/auth-context";
import { Button } from "@/components/ui/button";
import { useTranslations } from "@/i18n/locale-context";

export function AdminSidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAdmin, loading, signOut } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [signingOut, setSigningOut] = useState(false);
  const { t } = useTranslations();

  const adminLinks = useMemo(
    () => [
      { href: "/admin", label: t("admin.analytics"), icon: LayoutDashboard },
      { href: "/admin/resources", label: t("admin.resources"), icon: FolderOpen },
      { href: "/admin/categories", label: t("admin.categories"), icon: Tags },
      { href: "/admin/facilities", label: t("admin.facilities"), icon: Building2 },
      { href: "/admin/users", label: t("admin.users"), icon: Users },
      { href: "/admin/homepage", label: t("admin.homepage"), icon: Home },
      { href: "/admin/cms", label: t("admin.sitePages"), icon: FileText },
      { href: "/admin/announcements", label: t("admin.announcements"), icon: Megaphone },
      { href: "/admin/faqs", label: t("admin.faqs"), icon: HelpCircle },
    ],
    [t]
  );

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] w-full items-center justify-center">
        <p className="text-lg text-muted-foreground">{t("common.loading")}</p>
      </div>
    );
  }

  if (!user || !isAdmin) {
    return null;
  }

  const NavContent = () => (
    <>
      <div className="mb-8 px-4">
        <p className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          {t("admin.portal")}
        </p>
        <p className="mt-1 text-base font-medium">{user.full_name || user.email}</p>
      </div>
      <nav aria-label={t("admin.portal")}>
        <ul className="space-y-1 px-2">
          {adminLinks.map(({ href, label, icon: Icon }) => {
            const isSitePagesSection =
              href === "/admin/cms" &&
              (pathname === "/admin/cms" ||
                pathname.startsWith("/admin/about") ||
                pathname.startsWith("/admin/contact") ||
                pathname.startsWith("/admin/legal"));
            const isActive = pathname === href || isSitePagesSection;

            return (
            <li key={href}>
              <Link
                href={href}
                onClick={() => setMobileOpen(false)}
                className={cn(
                  "flex min-h-[48px] cursor-pointer items-center gap-3 rounded-xl px-4 py-3 text-base font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-foreground hover:bg-muted"
                )}
                aria-current={isActive ? "page" : undefined}
              >
                <Icon className="h-5 w-5" aria-hidden="true" />
                {label}
              </Link>
            </li>
            );
          })}
        </ul>
      </nav>
      <div className="mt-auto border-t border-border p-4">
        <Link
          href="/"
          className="mb-2 flex min-h-[44px] cursor-pointer items-center gap-2 rounded-xl px-4 py-2 text-base text-muted-foreground hover:bg-muted"
        >
          {t("admin.backToSite")}
        </Link>
        <Button
          variant="outline"
          className="w-full"
          loading={signingOut}
          onClick={async () => {
            setSigningOut(true);
            try {
              await signOut();
              router.replace("/login");
              router.refresh();
            } finally {
              setSigningOut(false);
            }
          }}
        >
          <LogOut className="h-4 w-4" aria-hidden="true" />
          {t("nav.signOut")}
        </Button>
      </div>
    </>
  );

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <button
        type="button"
        className="fixed bottom-4 right-4 z-50 flex h-14 w-14 cursor-pointer items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg lg:hidden"
        onClick={() => setMobileOpen(!mobileOpen)}
        aria-label={mobileOpen ? t("common.closeMenu") : t("common.openMenu")}
      >
        {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </button>

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-border bg-card pt-20 transition-transform lg:static lg:translate-x-0 lg:pt-6",
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <NavContent />
      </aside>

      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/40 lg:hidden"
          onClick={() => setMobileOpen(false)}
          aria-hidden="true"
        />
      )}
    </div>
  );
}
