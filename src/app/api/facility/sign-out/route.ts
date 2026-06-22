import { NextResponse } from "next/server";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { verifyFacilityProfileBinding } from "@/lib/facility/data";
import { readFacilitySession } from "@/lib/facility/session";
import { clearPreferencesSetCookie } from "@/lib/user-preferences/cookie-options";

/** End auth for the current facility tablet session; keeps the facility session cookie. */
export async function POST() {
  if (!isSupabaseConfigured()) {
    return NextResponse.json({ success: true });
  }

  const supabase = await createClient();
  if (supabase) {
    await supabase.auth.signOut();
  }

  const response = NextResponse.json({ success: true });
  response.headers.append("Set-Cookie", clearPreferencesSetCookie());
  return response;
}
