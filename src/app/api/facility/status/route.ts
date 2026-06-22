import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { facilityAccountExistsByPinHash } from "@/lib/facility/data";
import { readFacilitySession } from "@/lib/facility/session";
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

  const hasAccount = await facilityAccountExistsByPinHash(
    session.facilityId,
    session.pinHash
  );

  return NextResponse.json({
    facilityId: session.facilityId,
    hasAccount,
  });
}
