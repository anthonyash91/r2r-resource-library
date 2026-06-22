import { FacilityForgotPasswordForm } from "@/components/facility/facility-forgot-password-form";
import { getServerTranslator } from "@/i18n/server";
import type { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return { title: t("facility.resetTitle") };
}

export default function FacilityForgotPasswordPage() {
  return <FacilityForgotPasswordForm />;
}
