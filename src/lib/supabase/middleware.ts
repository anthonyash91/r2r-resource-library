import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";
import { getAdminSession } from "@/lib/admin-auth";
import { enforceApiRouteAccess } from "@/lib/api-auth";

export async function updateSession(request: NextRequest) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!url || !key) {
    return NextResponse.next({ request });
  }

  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(url, key, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet) {
        cookiesToSet.forEach(({ name, value }) =>
          request.cookies.set(name, value)
        );
        supabaseResponse = NextResponse.next({ request });
        cookiesToSet.forEach(({ name, value, options }) =>
          supabaseResponse.cookies.set(name, value, options)
        );
      },
    },
  });

  await supabase.auth.getUser();

  const pathname = request.nextUrl.pathname;

  const apiBlock = await enforceApiRouteAccess(request, supabase);
  if (apiBlock) {
    return apiBlock;
  }

  if (pathname.startsWith("/admin")) {
    const session = await getAdminSession(supabase);
    if (!session) {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (user) {
        return NextResponse.redirect(new URL("/dashboard", request.url));
      }

      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("next", pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  if (
    request.nextUrl.searchParams.has("facility") &&
    request.nextUrl.searchParams.has("pin") &&
    !request.nextUrl.pathname.startsWith("/api/facility/enter")
  ) {
    const nextUrl = request.nextUrl.clone();
    nextUrl.searchParams.delete("facility");
    nextUrl.searchParams.delete("pin");
    const enterUrl = new URL("/api/facility/enter", request.url);
    enterUrl.searchParams.set("facility", request.nextUrl.searchParams.get("facility")!);
    enterUrl.searchParams.set("pin", request.nextUrl.searchParams.get("pin")!);
    enterUrl.searchParams.set(
      "next",
      `${nextUrl.pathname}${nextUrl.search ? `?${nextUrl.searchParams.toString()}` : ""}`
    );
    return NextResponse.redirect(enterUrl);
  }

  return supabaseResponse;
}
