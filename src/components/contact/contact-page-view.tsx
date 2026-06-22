"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { BookOpen, HelpCircle, Mail, MessageCircle } from "lucide-react";
import { PageHeroBand } from "@/components/layout/page-hero-band";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dropdown } from "@/components/ui/dropdown";
import { Card } from "@/components/ui/card";
import { cn, pageSectionPadding, pageSectionSubheadingClass } from "@/lib/utils";
import { buildResourcesPageHref } from "@/lib/resources-page";
import type { ContactPageContent } from "@/lib/contact-content-fields";
import { useTranslations } from "@/i18n/locale-context";

interface ContactPageViewProps {
  content: ContactPageContent;
  initialSubject?: string;
}

const SUBJECT_VALUES = ["general", "suggest-resource", "report-info", "account"] as const;

function isValidSubject(value: string): value is (typeof SUBJECT_VALUES)[number] {
  return SUBJECT_VALUES.includes(value as (typeof SUBJECT_VALUES)[number]);
}

export function ContactPageView({ content, initialSubject }: ContactPageViewProps) {
  const { t } = useTranslations();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("general");
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (initialSubject && isValidSubject(initialSubject)) {
      setSubject(initialSubject);
    }
  }, [initialSubject]);

  const subjectOptions = useMemo(
    () =>
      SUBJECT_VALUES.map((value) => ({
        value,
        label: t(`contact.subject.${value}`),
      })),
    [t]
  );

  const helpLinks = useMemo(
    () => [
      {
        href: "/faq",
        icon: HelpCircle,
        title: content.helpLinks.faqs.title,
        description: content.helpLinks.faqs.description,
      },
      {
        href: buildResourcesPageHref(),
        icon: BookOpen,
        title: content.helpLinks.resources.title,
        description: content.helpLinks.resources.description,
      },
      {
        href: "/contact?subject=suggest-resource",
        icon: MessageCircle,
        title: content.helpLinks.suggest.title,
        description: content.helpLinks.suggest.description,
      },
    ],
    [content.helpLinks]
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSending(true);
    await new Promise((resolve) => setTimeout(resolve, 600));
    setSubmitted(true);
    setSending(false);
  };

  return (
    <div>
      <PageHeroBand
        icon={Mail}
        title={content.heroTitle}
        description={content.heroDescription}
      />

      <div className={cn("app-band-alt", pageSectionPadding)}>
        <div className="mx-auto max-w-6xl">
          <div className="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)] lg:items-start">
            <Card className="p-6 sm:p-8">
              <h2 className="mb-6 text-2xl font-bold text-foreground">{content.formTitle}</h2>

              {submitted ? (
                <p
                  role="status"
                  className="rounded-xl bg-secondary px-5 py-4 text-base leading-relaxed text-foreground"
                >
                  {t("contact.submitSuccess")}
                </p>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-5">
                  <div className="grid gap-5 sm:grid-cols-2">
                    <Input
                      label={t("contact.yourName")}
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder={t("contact.namePlaceholder")}
                      autoComplete="name"
                      required
                    />
                    <Input
                      label={t("contact.emailAddress")}
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder={t("contact.emailPlaceholder")}
                      autoComplete="email"
                      required
                    />
                  </div>

                  <Dropdown
                    label={t("contact.subjectLabel")}
                    placeholder={t("contact.subject.general")}
                    value={subject}
                    onChange={setSubject}
                    options={subjectOptions}
                    searchable={false}
                  />

                  <div>
                    <label
                      htmlFor="contact-message"
                      className="mb-2 block text-base font-semibold text-foreground"
                    >
                      {t("contact.messageLabel")}
                    </label>
                    <textarea
                      id="contact-message"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      placeholder={t("contact.messagePlaceholder")}
                      required
                      rows={6}
                      className="w-full rounded-xl border-2 border-border bg-card px-4 py-3 text-base text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-2 focus:ring-ring/30"
                    />
                  </div>

                  <Button type="submit" size="lg" className="w-full" loading={sending}>
                    {sending ? t("contact.sending") : t("contact.sendMessage")}
                  </Button>
                </form>
              )}
            </Card>

            <div className="space-y-6">
              <Card className="p-6 sm:p-7">
                <h2 className={cn("mb-5", pageSectionSubheadingClass)}>{content.otherWaysTitle}</h2>
                <ul className="space-y-5">
                  {helpLinks.map(({ href, icon: Icon, title: linkTitle, description: linkDesc }) => (
                    <li key={href}>
                      <Link
                        href={href}
                        className={cn(
                          "group flex items-center gap-4 rounded-xl transition-colors",
                          "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring"
                        )}
                      >
                        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-secondary text-primary">
                          <Icon className="h-5 w-5" aria-hidden="true" />
                        </span>
                        <span>
                          <span className="block font-semibold text-foreground group-hover:text-primary">
                            {linkTitle}
                          </span>
                          <span className="mt-0.5 block text-sm leading-relaxed text-muted-foreground">
                            {linkDesc}
                          </span>
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </Card>

              <Card className="border-primary/15 bg-secondary/60 p-6 sm:p-7">
                <h2 className={cn("mb-3", pageSectionSubheadingClass)}>{content.responseTimeTitle}</h2>
                <p className="text-base leading-relaxed text-foreground/90">
                  {content.responseTimeBody}
                </p>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
