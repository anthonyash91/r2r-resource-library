"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

export interface HomeFaqItem {
  id: string;
  question: string;
  answer: string;
}

export function HomeFaqAccordion({ faqs }: { faqs: HomeFaqItem[] }) {
  const [openId, setOpenId] = useState<string | null>(faqs[0]?.id ?? null);

  if (faqs.length === 0) return null;

  return (
    <div>
      {faqs.map((faq, index) => {
        const isOpen = openId === faq.id;
        const num = String(index + 1).padStart(2, "0");

        return (
          <div
            key={faq.id}
            className="flex gap-4 border-b border-[var(--line)] py-5 sm:gap-[18px] sm:py-[22px]"
          >
            <div
              className={cn(
                "flex h-[34px] w-[34px] shrink-0 items-center justify-center rounded-[9px] font-heading text-[13px] font-extrabold",
                isOpen ? "bg-primary text-primary-foreground" : "bg-[#EFEAFE] text-[var(--accent-ink)]"
              )}
            >
              {num}
            </div>
            <div className="min-w-0 flex-1">
              <button
                type="button"
                className="flex min-h-[34px] w-full cursor-pointer items-center justify-between gap-4 text-left"
                onClick={() => setOpenId(isOpen ? null : faq.id)}
                aria-expanded={isOpen}
                aria-controls={`home-faq-${faq.id}`}
              >
                <span
                  className={cn(
                    "font-heading text-base font-bold leading-snug sm:text-[17px]",
                    isOpen ? "text-[var(--accent-ink)]" : "text-foreground"
                  )}
                >
                  {faq.question}
                </span>
                <span
                  className={cn(
                    "shrink-0 text-xl font-medium leading-none",
                    isOpen ? "text-[var(--accent-ink)]" : "text-foreground"
                  )}
                  aria-hidden="true"
                >
                  {isOpen ? "–" : "+"}
                </span>
              </button>
              {isOpen ? (
                <div
                  id={`home-faq-${faq.id}`}
                  className="mt-3 rounded-xl bg-[#F4F4F8] px-[17px] py-[15px]"
                >
                  <p className="text-[15px] leading-relaxed text-muted-foreground">{faq.answer}</p>
                </div>
              ) : null}
            </div>
          </div>
        );
      })}
    </div>
  );
}
