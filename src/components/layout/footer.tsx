import Link from "next/link";
import { BookOpen } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";

const RESOURCE_CATEGORY_SLUGS = [
  "housing",
  "employment",
  "healthcare",
  "legal-aid",
  "mental-health",
] as const;

const footerLinkClass =
  "text-sm text-[var(--footer-muted)] transition-colors hover:text-[var(--footer-foreground)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--footer-accent)] rounded";

const footerHeadingClass =
  "mb-4 text-xs font-semibold uppercase tracking-wider text-[var(--footer-foreground)]";

export async function Footer() {
  const { t } = await getServerTranslator();
  const year = new Date().getFullYear();

  const resourceLinks = [
    ...RESOURCE_CATEGORY_SLUGS.map((slug) => ({
      href: `/resources?category=${slug}`,
      label: t(`categories.${slug}.name`),
    })),
    { href: "/resources", label: t("footer.allCategories") },
  ];

  const helpLinks = [
    { href: "/#how-it-works-heading", label: t("footer.howItWorks") },
    { href: "/faq", label: t("footer.helpFaq") },
    { href: "/about", label: t("footer.contactUs") },
    { href: "/faq", label: t("footer.reportIssue") },
  ];

  const accountLinks = [
    { href: "/login", label: t("footer.signIn") },
    { href: "/signup", label: t("footer.createAccount") },
    { href: "/dashboard", label: t("footer.myDashboard") },
    { href: "/saved", label: t("footer.savedResources") },
  ];

  const legalLinks = [
    { href: "/about", label: t("footer.privacyPolicy") },
    { href: "/about", label: t("footer.termsOfUse") },
    { href: "/about", label: t("footer.accessibility") },
  ];

  return (
    <footer className="footer-surface mt-auto">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-[minmax(0,1.5fr)_repeat(3,minmax(0,1fr))] lg:gap-12">
          <div className="sm:col-span-2 lg:col-span-1">
            <div className="mb-5 flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                <BookOpen className="h-5 w-5" aria-hidden="true" />
              </div>
              <div>
                <span className="block text-lg font-bold leading-tight text-[var(--footer-foreground)]">
                  {t("nav.brandName")}
                </span>
                <span className="mt-0.5 block text-sm font-medium text-[var(--footer-accent)]">
                  {t("footer.tagline")}
                </span>
              </div>
            </div>
            <p className="mb-4 max-w-md text-sm leading-relaxed text-[var(--footer-muted)]">
              {t("footer.description")}
            </p>
            <p className="text-sm text-[var(--footer-muted)]">
              {t("footer.builtWithLovePrefix")}{" "}
              <span className="text-[var(--footer-heart)]" aria-hidden="true">
                ♡
              </span>{" "}
              {t("footer.builtWithLoveSuffix")}
            </p>
          </div>

          <div>
            <h2 className={footerHeadingClass}>{t("footer.resourcesHeading")}</h2>
            <ul className="space-y-2.5">
              {resourceLinks.map(({ href, label }) => (
                <li key={`${href}-${label}`}>
                  <Link href={href} className={footerLinkClass}>
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h2 className={footerHeadingClass}>{t("footer.helpHeading")}</h2>
            <ul className="space-y-2.5">
              {helpLinks.map(({ href, label }) => (
                <li key={`${href}-${label}`}>
                  <Link href={href} className={footerLinkClass}>
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h2 className={footerHeadingClass}>{t("footer.accountHeading")}</h2>
            <ul className="space-y-2.5">
              {accountLinks.map(({ href, label }) => (
                <li key={href}>
                  <Link href={href} className={footerLinkClass}>
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-12 flex flex-col gap-4 border-t border-[var(--footer-border)] pt-6 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-[var(--footer-muted)]">
            {t("footer.copyright", { year })}
          </p>
          <div className="flex flex-wrap gap-x-6 gap-y-2">
            {legalLinks.map(({ href, label }) => (
              <Link key={label} href={href} className={footerLinkClass}>
                {label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
