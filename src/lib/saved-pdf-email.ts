export const SAVED_PDF_EMAIL_LIMIT = 3;

export interface SavedPdfEmailStatus {
  sent: number;
  limit: number | null;
  remaining: number | null;
  unlimited?: boolean;
}

export function getSavedPdfEmailStatus(
  sent: number,
  options?: { unlimited?: boolean }
): SavedPdfEmailStatus {
  const safeSent = Math.max(0, sent);

  if (options?.unlimited) {
    return {
      sent: safeSent,
      limit: null,
      remaining: null,
      unlimited: true,
    };
  }

  return {
    sent: safeSent,
    limit: SAVED_PDF_EMAIL_LIMIT,
    remaining: Math.max(0, SAVED_PDF_EMAIL_LIMIT - safeSent),
  };
}

export function isAdminPdfEmailUnlimited(role: string | undefined | null): boolean {
  return role === "admin";
}
