import Link from "next/link";
import {
  Accessibility,
  CircleCheck,
  Eye,
  Keyboard,
  Mail,
  Smartphone,
  Volume2,
} from "lucide-react";
import { PageHeroBand } from "@/components/layout/page-hero-band";
import { Card } from "@/components/ui/card";
import { cn, pageSectionPadding, checkIconClass, pageSectionSubheadingClass } from "@/lib/utils";
import type { AccessibilityPageContent } from "@/lib/legal-content";
import { getServerTranslator } from "@/i18n/server";

const FEATURE_ICONS = {
  keyboard: Keyboard,
  screenReader: Eye,
  plainLanguage: Volume2,
  mobile: Smartphone,
} as const;

interface AccessibilityPageViewProps {
  content: AccessibilityPageContent;
}

export async function AccessibilityPageView({ content }: AccessibilityPageViewProps) {
  const { t } = await getServerTranslator();

  return (
    <div>
      <PageHeroBand
        icon={Accessibility}
        title={content.title}
        description={content.description}
      />

      <section className={cn("bg-muted", pageSectionPadding)}>
        <div className="mx-auto max-w-3xl space-y-10">
          <article className="rounded-2xl border border-border bg-card p-6 sm:p-8 lg:p-10">
            <section aria-labelledby="accessibility-commitment-heading">
              <h2
                id="accessibility-commitment-heading"
                className="mb-4 text-xl font-bold text-foreground sm:text-2xl"
              >
                {content.commitmentTitle}
              </h2>
              <p className="text-base leading-[1.75] text-foreground/90">{content.commitmentP1}</p>
              <p className="mt-4 text-base leading-[1.75] text-foreground/90">{content.commitmentP2}</p>
            </section>

            <section className="mt-10" aria-labelledby="accessibility-wcag-heading">
              <h2
                id="accessibility-wcag-heading"
                className="mb-5 text-xl font-bold text-foreground sm:text-2xl"
              >
                {content.wcagTitle}
              </h2>
              <ul className="space-y-4">
                {content.principles.map(({ key, title, body }) => (
                  <li key={key} className="flex items-center gap-3">
                    <CircleCheck className={cn("h-5 w-5 shrink-0", checkIconClass)} aria-hidden="true" />
                    <span className="text-base leading-relaxed text-foreground">
                      <span className="font-semibold">{title}</span>
                      {": "}
                      {body}
                    </span>
                  </li>
                ))}
              </ul>
            </section>

            <section className="mt-10" aria-labelledby="accessibility-features-heading">
              <h2
                id="accessibility-features-heading"
                className="mb-5 text-xl font-bold text-foreground sm:text-2xl"
              >
                {content.featuresTitle}
              </h2>
              <div className="grid gap-4 sm:grid-cols-2">
                {content.features.map(({ key, title, body }) => {
                  const Icon = FEATURE_ICONS[key];
                  return (
                    <Card key={key} className="p-5 sm:p-6">
                      <span className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-secondary text-primary">
                        <Icon className="h-5 w-5" aria-hidden="true" />
                      </span>
                      <h3 className={cn("mb-2", pageSectionSubheadingClass)}>{title}</h3>
                      <p className="text-sm leading-relaxed text-muted-foreground sm:text-base">
                        {body}
                      </p>
                    </Card>
                  );
                })}
              </div>
            </section>

            <section className="mt-10" aria-labelledby="accessibility-limitations-heading">
              <h2
                id="accessibility-limitations-heading"
                className="mb-3 text-xl font-bold text-foreground sm:text-2xl"
              >
                {content.limitationsTitle}
              </h2>
              <p className="text-base leading-[1.75] text-foreground/90">{content.limitationsBody}</p>
            </section>

            <p className="mt-10 text-sm text-muted-foreground">
              {t("legal.lastUpdated", { date: content.lastUpdatedDate })}
            </p>
          </article>

          <Card className="flex flex-col gap-5 border-primary/15 bg-secondary/60 p-6 sm:flex-row sm:items-center sm:p-8">
            <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-card text-primary">
              <Mail className="h-6 w-6" aria-hidden="true" />
            </span>
            <div className="flex-1">
              <h2 className="mb-2 text-lg font-bold text-foreground">{content.reportTitle}</h2>
              <p className="text-base leading-relaxed text-foreground/90">{content.reportBody}</p>
            </div>
            <Link
              href="/contact"
              className={cn(
                "inline-flex min-h-[48px] shrink-0 cursor-pointer items-center justify-center rounded-xl bg-primary px-6 py-3 text-base font-semibold text-primary-foreground transition-colors",
                "hover:bg-primary-hover focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
              )}
            >
              {t("footer.contactUs")}
            </Link>
          </Card>
        </div>
      </section>
    </div>
  );
}
