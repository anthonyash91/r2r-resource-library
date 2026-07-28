import Link from "next/link";
import { getServerTranslator } from "@/i18n/server";
import { getSiteBranding } from "@/lib/data";
import { FooterBrandingLockup } from "@/components/layout/footer-branding-lockup";
import { FooterLocaleLink } from "@/components/layout/footer-locale-link";
import { LibraryDisclaimer } from "@/components/resources/library-disclaimer";
import { buildResourcesPageHref } from "@/lib/resources-page";

const RESOURCE_CATEGORY_SLUGS = [
  "housing",
  "employment",
  "education",
  "substance-abuse-recovery",
  "legal-aid",
] as const;

const footerLinkClass =
  "block text-[15px] leading-none text-[var(--footer-subheader)] transition-colors hover:text-[var(--footer-foreground)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--footer-accent)] rounded";

const footerHeadingClass =
  "mb-4 font-heading text-sm font-bold leading-none text-[var(--footer-foreground)]";

export async function Footer() {
  const { t } = await getServerTranslator();
  const branding = await getSiteBranding();
  const year = new Date().getFullYear();

  const resourceLinks = RESOURCE_CATEGORY_SLUGS.map((slug) => ({
    href: buildResourcesPageHref({ category: slug }, "results"),
    label: t(`categories.${slug}.shortName`),
  }));

  const organizationLinks = [
    { href: "/about", label: t("footer.aboutUs") },
    { href: "/contact", label: t("nav.forCaseWorkers") },
    { href: "/contact", label: t("footer.partnerWithUs") },
    { href: "/contact", label: t("footer.suggestResource") },
    { href: "/contact", label: t("footer.contactUs") },
  ];

  const helpLinks = [
    { href: buildResourcesPageHref(), label: t("footer.findResources") },
    { href: "/faq", label: t("footer.crisisLines") },
    { href: "/faq", label: t("footer.shortFaq") },
    { href: "/accessibility", label: t("footer.accessibility") },
    { href: "/accessibility", label: t("footer.languages") },
  ];

  const legalLinks = [
    { href: "/privacy", label: t("footer.privacyPolicy") },
    { href: "/terms", label: t("footer.termsOfUse") },
    { href: "/accessibility", label: t("footer.accessibility") },
  ];

  return (
    <footer className="footer-surface mt-auto">
      <div className="mx-auto max-w-[1180px] px-4 py-10 sm:px-9">
        <div className="footer-main">
          <div className="min-w-0 max-w-[400px]">
            <FooterBrandingLockup
              brandName={branding.brandName}
              tagline={branding.footerTagline}
              variant="compact"
              className="mb-4"
            />
            <p className="text-[15px] leading-[1.6] text-[var(--footer-muted)]">
              {branding.footerDescription}
            </p>
          </div>

          <div className="footer-link-columns">
            <div className="min-w-0">
              <h2 className={footerHeadingClass}>{t("footer.resourcesHeading")}</h2>
              <div className="footer-link-column">
                {resourceLinks.map(({ href, label }) => (
                  <Link key={href + label} href={href} className={footerLinkClass}>
                    {label}
                  </Link>
                ))}
              </div>
            </div>

            <div className="min-w-0">
              <h2 className={footerHeadingClass}>{t("footer.organizationHeading")}</h2>
              <div className="footer-link-column">
                {organizationLinks.map(({ href, label }) => (
                  <Link key={label} href={href} className={footerLinkClass}>
                    {label}
                  </Link>
                ))}
              </div>
            </div>

            <div className="min-w-0">
              <h2 className={footerHeadingClass}>{t("footer.getHelpHeading")}</h2>
              <div className="footer-link-column">
                {helpLinks.map(({ href, label }) => (
                  <Link key={label} href={href} className={footerLinkClass}>
                    {label}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="mx-auto max-w-[1180px] px-4 pt-[18px] sm:px-9">
          <LibraryDisclaimer
            variant="footer"
            className="max-w-[780px] text-xs leading-[1.6] text-[#767c92]"
          />
        </div>

        <div className="mx-auto flex max-w-[1180px] flex-col gap-3.5 px-4 pt-5 pb-10 sm:flex-row sm:items-center sm:justify-between sm:px-9">
          <p className="text-[13px] leading-none text-[var(--footer-muted)]">
            {t("footer.copyright", { year })}
          </p>
          <div className="flex flex-wrap items-center gap-[22px]">
            {legalLinks.map(({ href, label }) => (
              <Link
                key={label}
                href={href}
                className="text-[13px] leading-none text-[var(--footer-muted)] transition-colors hover:text-[var(--footer-foreground)]"
              >
                {label}
              </Link>
            ))}
            <FooterLocaleLink />
          </div>
        </div>
      </div>
    </footer>
  );
}
