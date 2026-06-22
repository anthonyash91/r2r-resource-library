import { FacilityLoginForm } from "@/components/facility/facility-login-form";
import { getServerTranslator } from "@/i18n/server";
import type { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return { title: t("facility.loginTitle") };
}

export default function FacilityLoginPage() {
  return <FacilityLoginForm />;
}
