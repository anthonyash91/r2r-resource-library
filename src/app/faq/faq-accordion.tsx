"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Faq } from "@/types";

export function FaqAccordion({ faqs }: { faqs: Faq[] }) {
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <div className="space-y-3">
      {faqs.map((faq) => {
        const isOpen = openId === faq.id;
        return (
          <div
            key={faq.id}
            className="rounded-xl border border-border bg-card overflow-hidden"
          >
            <button
              type="button"
              className="flex w-full min-h-[56px] cursor-pointer items-center justify-between gap-4 px-6 py-4 text-left text-base font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
              onClick={() => setOpenId(isOpen ? null : faq.id)}
              aria-expanded={isOpen}
              aria-controls={`faq-answer-${faq.id}`}
            >
              {faq.question}
              <ChevronDown
                className={cn("h-5 w-5 shrink-0 transition-transform", isOpen && "rotate-180")}
                aria-hidden="true"
              />
            </button>
            {isOpen && (
              <div
                id={`faq-answer-${faq.id}`}
                className="border-t border-border px-6 py-4 text-base text-muted-foreground"
              >
                {faq.answer}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
