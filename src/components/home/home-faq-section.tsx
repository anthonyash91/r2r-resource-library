import Link from "next/link";
import { getFaqs } from "@/lib/data";
import { getServerTranslator } from "@/i18n/server";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { HomeFaqAccordion } from "@/components/home/home-faq-accordion";

export async function HomeFaqSection() {
  const { t } = await getServerTranslator();
  const faqs = await getFaqs();
  const items = faqs.slice(0, 6).map((faq) => ({
    id: faq.id,
    question: faq.question,
    answer: faq.answer,
  }));

  if (items.length === 0) return null;

  return (
    <section
      className="mx-auto max-w-[820px] px-4 py-12 sm:px-9 sm:py-16"
      aria-labelledby="home-faq-heading"
    >
      <ScrollReveal variant="fade-up">
        <header className="mb-10 text-center">
          <h2
            id="home-faq-heading"
            className="font-heading text-[32px] font-extrabold tracking-tight text-foreground sm:text-[38px]"
          >
            {t("home.faqSectionTitle")}
          </h2>
          <p className="mx-auto mt-4 max-w-[520px] text-[17px] leading-relaxed text-muted-foreground">
            {t("home.faqSectionSubtitle")}
          </p>
        </header>
      </ScrollReveal>

      <ScrollReveal variant="fade-up" delay={75}>
        <HomeFaqAccordion faqs={items} />
      </ScrollReveal>

      <ScrollReveal variant="fade-up" delay={150}>
        <div className="mt-10 rounded-[18px] border border-[var(--line)] bg-[var(--soft)] p-8 text-center sm:p-[34px]">
          <h3 className="font-heading text-[22px] font-extrabold text-foreground">
            {t("faq.stillNeedHelpTitle")}
          </h3>
          <p className="mx-auto mt-2.5 max-w-[420px] text-base leading-relaxed text-muted-foreground">
            {t("faq.stillNeedHelpBody")}
          </p>
          <Link
            href="/contact"
            className="mt-5 inline-flex min-h-[44px] items-center rounded-[11px] bg-primary px-6 py-3.5 font-heading text-[15px] font-bold text-primary-foreground transition-colors hover:bg-primary-hover"
          >
            {t("footer.contactUs")}
          </Link>
        </div>
      </ScrollReveal>
    </section>
  );
}
