import Link from "next/link";
import { getServerTranslator } from "@/i18n/server";
import { getSiteBranding } from "@/lib/data";
import { FooterBrandingLockup } from "@/components/layout/footer-branding-lockup";
import { buildResourcesPageHref } from "@/lib/resources-page";

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

const footerLinkColumnClass =
  "min-w-0 text-left lg:w-max lg:justify-self-end";

export async function Footer() {
  const { t } = await getServerTranslator();
  const branding = await getSiteBranding();
  const year = new Date().getFullYear();

  const resourceLinks = [
    ...RESOURCE_CATEGORY_SLUGS.map((slug) => ({
      href: buildResourcesPageHref({ category: slug }, "results"),
      label: t(`categories.${slug}.name`),
    })),
    { href: buildResourcesPageHref(), label: t("footer.allCategories") },
  ];

  const helpLinks = [
    { href: "/#how-it-works-heading", label: t("footer.howItWorks") },
    { href: "/faq", label: t("footer.helpFaq") },
    { href: "/about", label: t("footer.aboutUs") },
    { href: "/contact", label: t("footer.contactUs") },
    { href: "/faq", label: t("footer.reportIssue") },
  ];

  const accountLinks = [
    { href: "/login", label: t("footer.signIn") },
    { href: "/signup", label: t("footer.createAccount") },
    { href: "/dashboard", label: t("footer.myDashboard") },
    { href: "/saved", label: t("footer.savedResources") },
  ];

  const legalLinks = [
    { href: "/privacy", label: t("footer.privacyPolicy") },
    { href: "/terms", label: t("footer.termsOfUse") },
    { href: "/accessibility", label: t("footer.accessibility") },
  ];

  return (
    <footer className="footer-surface mt-auto">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-[minmax(0,1.5fr)_repeat(3,minmax(0,1fr))] lg:gap-12">
          <div className="min-w-0 sm:col-span-2 lg:col-span-1">
            <FooterBrandingLockup
              brandName={branding.brandName}
              tagline={branding.footerTagline}
              className="mb-5"
            />
            <p className="mb-4 max-w-md text-sm leading-relaxed text-[var(--footer-muted)]">
              {branding.footerDescription}
            </p>
            <p className="text-sm text-[var(--footer-muted)]">
              {t("footer.builtWithLovePrefix")}{" "}
              <span className="text-[var(--footer-heart)]" aria-hidden="true">
                ♡
              </span>{" "}
              {t("footer.builtWithLoveSuffix")}
            </p>
          </div>

          <div className={footerLinkColumnClass}>
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

          <div className={footerLinkColumnClass}>
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

          <div className={footerLinkColumnClass}>
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
