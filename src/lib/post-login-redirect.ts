export function resolvePostLoginPath(options: {
  next: string | null;
  isAdmin: boolean;
}): string {
  const { next, isAdmin } = options;

  if (next?.startsWith("/")) {
    if (next.startsWith("/admin") && !isAdmin) {
      return "/dashboard";
    }
    return next;
  }

  return isAdmin ? "/admin" : "/dashboard";
}
