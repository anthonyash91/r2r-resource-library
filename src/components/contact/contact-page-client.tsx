"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { ContactPageView } from "@/components/contact/contact-page-view";
import type { ContactPageContent } from "@/lib/contact-content-fields";

interface ContactPageClientProps {
  content: ContactPageContent;
}

function ContactPageContent({ content }: ContactPageClientProps) {
  const searchParams = useSearchParams();
  const subjectParam = searchParams.get("subject") ?? undefined;

  return <ContactPageView content={content} initialSubject={subjectParam} />;
}

export function ContactPageClient({ content }: ContactPageClientProps) {
  return (
    <Suspense fallback={<ContactPageView content={content} />}>
      <ContactPageContent content={content} />
    </Suspense>
  );
}
