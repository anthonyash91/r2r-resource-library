"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Faq } from "@/types";

export function FaqAccordion({ faqs }: { faqs: Faq[] }) {
  const [openId, setOpenId] = useState<string | null>(null);

  if (faqs.length === 0) {
    return null;
  }

  return (
    <div className="space-y-3">
      {faqs.map((faq) => {
        const isOpen = openId === faq.id;
        return (
          <div
            key={faq.id}
            className={cn(
              "overflow-hidden rounded-2xl border border-border bg-card transition-colors",
              isOpen && "border-primary/20"
            )}
          >
            <button
              type="button"
              className={cn(
                "flex w-full min-h-[56px] cursor-pointer items-center justify-between gap-4 px-5 py-4 text-left text-base font-semibold text-foreground transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring sm:px-6",
                isOpen ? "bg-card hover:bg-card" : "hover:bg-muted/40"
              )}
              onClick={() => setOpenId(isOpen ? null : faq.id)}
              aria-expanded={isOpen}
              aria-controls={`faq-answer-${faq.id}`}
            >
              <span className="pr-2">{faq.question}</span>
              <ChevronDown
                className={cn(
                  "h-5 w-5 shrink-0 text-primary transition-transform duration-200",
                  isOpen && "rotate-180"
                )}
                aria-hidden="true"
              />
            </button>
            {isOpen ? (
              <div
                id={`faq-answer-${faq.id}`}
                className="border-t border-border/80 bg-secondary/30 px-5 pb-5 pt-4 sm:px-6 sm:pb-6"
              >
                <p className="text-base leading-[1.75] text-foreground/90">{faq.answer}</p>
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
