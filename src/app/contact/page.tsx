import type { Metadata } from "next";
import { ContactPageClient } from "@/components/contact/contact-page-client";
import { getContactPageContent } from "@/lib/data";

export async function generateMetadata(): Promise<Metadata> {
  const content = await getContactPageContent();

  return {
    title: content.heroTitle,
    description: content.heroDescription,
  };
}

export default async function ContactPage() {
  const content = await getContactPageContent();

  return <ContactPageClient content={content} />;
}
