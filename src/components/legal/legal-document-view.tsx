import Link from "next/link";
import type { LucideIcon } from "lucide-react";
import { PageHeroBand } from "@/components/layout/page-hero-band";
import { cn, pageSectionPadding } from "@/lib/utils";

export interface LegalSection {
  title: string;
  paragraphs?: string[];
  bullets?: string[];
  contactLink?: boolean;
}

interface LegalDocumentViewProps {
  icon: LucideIcon;
  title: string;
  description: string;
  intro: string;
  sections: LegalSection[];
  lastUpdated: string;
  contactLinkLabel: string;
  contactPrompt?: string;
}

export function LegalDocumentView({
  icon,
  title,
  description,
  intro,
  sections,
  lastUpdated,
  contactLinkLabel,
  contactPrompt,
}: LegalDocumentViewProps) {
  return (
    <div>
      <PageHeroBand icon={icon} title={title} description={description} />

      <section className={cn("bg-muted", pageSectionPadding)}>
        <div className="mx-auto max-w-3xl">
          <article className="rounded-2xl border border-border bg-card p-6 sm:p-8 lg:p-10">
            <div className="mb-8 rounded-xl border border-border bg-secondary/60 p-5 sm:p-6">
              <p className="text-base leading-relaxed text-foreground sm:text-lg">{intro}</p>
            </div>

            <div className="space-y-8">
              {sections.map((section) => (
                <section key={section.title}>
                  <h2 className="mb-3 text-lg font-bold text-foreground">{section.title}</h2>

                  {section.paragraphs?.map((paragraph) => (
                    <p
                      key={paragraph}
                      className="text-base leading-[1.75] text-foreground/90 [&+p]:mt-4"
                    >
                      {paragraph}
                    </p>
                  ))}

                  {section.contactLink && contactPrompt ? (
                    <p className="text-base leading-[1.75] text-foreground/90">
                      {contactPrompt}{" "}
                      <Link
                        href="/contact"
                        className={cn(
                          "font-semibold text-primary underline-offset-2 hover:text-primary-hover hover:underline",
                          "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
                        )}
                      >
                        {contactLinkLabel}
                      </Link>
                      .
                    </p>
                  ) : null}

                  {section.bullets && section.bullets.length > 0 ? (
                    <ul className="mt-4 space-y-2.5">
                      {section.bullets.map((item) => (
                        <li
                          key={item}
                          className="relative pl-5 text-base leading-[1.75] text-foreground/90 before:absolute before:left-0 before:top-[0.65em] before:h-1.5 before:w-1.5 before:rounded-full before:bg-primary"
                        >
                          {item}
                        </li>
                      ))}
                    </ul>
                  ) : null}
                </section>
              ))}
            </div>

            <p className="mt-10 text-sm text-muted-foreground">{lastUpdated}</p>
          </article>
        </div>
      </section>
    </div>
  );
}
