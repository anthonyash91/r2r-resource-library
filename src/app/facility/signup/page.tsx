import { FacilitySignupForm } from "@/components/facility/facility-signup-form";
import { getServerTranslator } from "@/i18n/server";
import type { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return { title: t("facility.signupTitle") };
}

export default function FacilitySignupPage() {
  return <FacilitySignupForm />;
}
