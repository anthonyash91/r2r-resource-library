import { notFound } from "next/navigation";
import { getLegalDocumentAdmin, getAccessibilityContentAdmin } from "@/lib/data";
import type { LegalDocumentSlug } from "@/lib/legal-content-fields";
import { LegalDocumentEditor } from "../legal-document-editor";
import { AccessibilityPageEditor } from "../accessibility-page-editor";

const LEGAL_DOCUMENTS = ["privacy", "terms", "accessibility"] as const;

type LegalDocumentParam = (typeof LEGAL_DOCUMENTS)[number];

interface AdminLegalPageProps {
  params: Promise<{ document: string }>;
}

export default async function AdminLegalPage({ params }: AdminLegalPageProps) {
  const { document } = await params;

  if (!LEGAL_DOCUMENTS.includes(document as LegalDocumentParam)) {
    notFound();
  }

  if (document === "accessibility") {
    const initial = await getAccessibilityContentAdmin();
    return <AccessibilityPageEditor initial={initial} />;
  }

  const initial = await getLegalDocumentAdmin(document as LegalDocumentSlug);
  return <LegalDocumentEditor document={document as LegalDocumentSlug} initial={initial} />;
}
