type AuthErrorLike = {
  message?: string;
  msg?: string;
  error_description?: string;
  code?: string;
  error_code?: string;
};

export function formatAuthError(error: unknown, fallback: string): string {
  if (!error) return fallback;
  if (typeof error === "string") return error.trim() || fallback;

  if (error instanceof Error) {
    const message = error.message.trim();
    if (message && message !== "{}") return message;
  }

  if (typeof error === "object" && error !== null) {
    const authError = error as AuthErrorLike;
    for (const key of ["message", "msg", "error_description"] as const) {
      const value = authError[key];
      if (typeof value === "string" && value.trim() && value.trim() !== "{}") {
        return value.trim();
      }
    }
  }

  return fallback;
}

export function isProfileSetupError(message: string): boolean {
  const normalized = message.toLowerCase();
  return (
    normalized.includes("database error saving new user") ||
    normalized.includes("unexpected_failure")
  );
}
