import Link from "next/link";
import { ArrowRight, Heart } from "lucide-react";
import { PageHeroBand } from "@/components/layout/page-hero-band";
import { cn, pageSectionPadding } from "@/lib/utils";
import { parseCmsContent } from "@/lib/parse-cms-content";

interface RelatedLink {
  href: string;
  label: string;
}

interface CmsPageViewProps {
  title: string;
  description: string;
  content: string;
  relatedLinks: RelatedLink[];
  exploreMoreLabel: string;
}

export function CmsPageView({
  title,
  description,
  content,
  relatedLinks,
  exploreMoreLabel,
}: CmsPageViewProps) {
  const blocks = parseCmsContent(content);
  const [leadBlock, ...restBlocks] = blocks;
  const leadParagraph = leadBlock?.type === "paragraph" ? leadBlock.text : null;
  const contentBlocks = leadParagraph ? restBlocks : blocks;

  return (
    <div>
      <PageHeroBand icon={Heart} title={title} description={description} />

      <section className={cn("app-band-alt", pageSectionPadding)}>
        <div className="mx-auto max-w-3xl">
          <article className="overflow-hidden rounded-2xl border border-border bg-card">
            <div className="p-6 sm:p-8 lg:p-10">
              {leadParagraph ? (
                <p className="mb-8 border-b border-border pb-8 text-xl leading-relaxed text-foreground">
                  {leadParagraph}
                </p>
              ) : null}

              <div className="divide-y divide-border">
                {contentBlocks.map((block, index) => {
                  if (block.type === "paragraph") {
                    return (
                      <p
                        key={`paragraph-${index}`}
                        className="py-6 text-base leading-[1.75] text-foreground/90 first:pt-0 last:pb-0"
                      >
                        {block.text}
                      </p>
                    );
                  }

                  return (
                    <section
                      key={`section-${block.title}-${index}`}
                      className="py-6 first:pt-0 last:pb-0"
                    >
                      {block.title ? (
                        <h2 className="mb-3 text-lg font-bold text-foreground">{block.title}</h2>
                      ) : null}

                      {block.body ? (
                        <p className="text-base leading-[1.75] text-foreground/90">{block.body}</p>
                      ) : null}

                      {block.items && block.items.length > 0 ? (
                        <ul
                          className={cn(
                            "ml-1 space-y-2.5",
                            (block.body || block.title) && "mt-4"
                          )}
                        >
                          {block.items.map((item) => (
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
                  );
                })}
              </div>
            </div>

            {relatedLinks.length > 0 ? (
              <footer className="border-t border-border bg-muted/50 px-6 py-5 sm:px-8">
                <p className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                  {exploreMoreLabel}
                </p>
                <div className="flex flex-wrap gap-2">
                  {relatedLinks.map(({ href, label }) => (
                    <Link
                      key={href}
                      href={href}
                      className={cn(
                        "inline-flex min-h-[44px] items-center gap-2 rounded-lg bg-card px-4 py-2 text-sm font-medium text-foreground ring-1 ring-border transition-colors",
                        "hover:bg-secondary hover:ring-primary/20 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring"
                      )}
                    >
                      {label}
                      <ArrowRight className="h-4 w-4 text-primary" aria-hidden="true" />
                    </Link>
                  ))}
                </div>
              </footer>
            ) : null}
          </article>
        </div>
      </section>
    </div>
  );
}
