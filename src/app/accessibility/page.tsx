import type { Metadata } from "next";
import { AccessibilityPageView } from "@/components/legal/accessibility-page-view";
import { getAccessibilityPageContent } from "@/lib/data";

export async function generateMetadata(): Promise<Metadata> {
  const content = await getAccessibilityPageContent();

  return {
    title: content.title,
    description: content.description,
  };
}

export default async function AccessibilityPage() {
  const content = await getAccessibilityPageContent();

  return <AccessibilityPageView content={content} />;
}
