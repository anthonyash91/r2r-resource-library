/** PostgREST returns at most this many rows per request unless `.range()` is used. */
export const SUPABASE_PAGE_SIZE = 1000;

type PageResult<T> = {
  data: T[] | null;
  error: { message: string } | null;
};

/**
 * Fetches every row for a Supabase query by paging with `.range(from, to)`.
 * Stops when a page returns fewer than {@link SUPABASE_PAGE_SIZE} rows.
 */
export async function fetchAllRows<T>(
  fetchPage: (range: { from: number; to: number }) => PromiseLike<PageResult<T>>
): Promise<{ data: T[]; error: PageResult<T>["error"] }> {
  const rows: T[] = [];
  let from = 0;

  while (true) {
    const to = from + SUPABASE_PAGE_SIZE - 1;
    const { data, error } = await fetchPage({ from, to });
    if (error) {
      return { data: rows, error };
    }

    const page = data ?? [];
    rows.push(...page);
    if (page.length < SUPABASE_PAGE_SIZE) {
      break;
    }
    from += SUPABASE_PAGE_SIZE;
  }

  return { data: rows, error: null };
}
