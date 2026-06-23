import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import {
  facilityAccountExistsByPinHash,
  getFacilityById,
} from "@/lib/facility/data";
import { getFacilitySessionProfilePreferences } from "@/lib/facility/session-preferences";
import { readFacilitySession } from "@/lib/facility/session";
import { maskPin } from "@/lib/facility/crypto";
import { LOCALE_COOKIE, type Locale } from "@/i18n/types";
import { createTranslator } from "@/i18n/translator";

async function getRequestLocale(): Promise<Locale> {
  const cookieStore = await cookies();
  const value = cookieStore.get(LOCALE_COOKIE)?.value;
  return value === "es" ? "es" : "en";
}

export async function GET() {
  const locale = await getRequestLocale();
  const { t } = createTranslator(locale);
  const session = await readFacilitySession();

  if (!session) {
    return NextResponse.json({ error: t("facility.sessionRequired") }, { status: 401 });
  }

  const facility = await getFacilityById(session.facilityId);
  if (!facility) {
    return NextResponse.json({ error: t("facility.sessionRequired") }, { status: 401 });
  }

  const hasAccount = await facilityAccountExistsByPinHash(
    session.facilityId,
    session.pinHash
  );

  const preferences = hasAccount
    ? await getFacilitySessionProfilePreferences(session.facilityId, session.pinHash)
    : null;

  return NextResponse.json({
    facilityId: session.facilityId,
    facilityName: facility.name,
    pinMasked: maskPin("*".repeat(session.pinLength)),
    hasAccount,
    preferences,
  });
}
