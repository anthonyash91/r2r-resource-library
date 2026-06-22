import { redirect } from "next/navigation";
import { GetStartedWizard } from "@/components/onboarding/get-started-wizard";
import { getServerTranslator } from "@/i18n/server";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import { hasCompletedOnboarding } from "@/lib/user-preferences/parse";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import type { Metadata } from "next";

interface PageProps {
  searchParams: Promise<{ edit?: string }>;
}

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getServerTranslator();
  return {
    title: t("onboarding.title"),
    description: t("onboarding.subtitle"),
  };
}

export default async function GetStartedPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const editMode = params.edit === "1";
  const prefs = await getServerUserPreferences();

  if (!editMode && hasCompletedOnboarding(prefs)) {
    let signedIn = false;
    if (isSupabaseConfigured()) {
      const supabase = await createClient();
      if (supabase) {
        const {
          data: { user },
        } = await supabase.auth.getUser();
        signedIn = Boolean(user);
      }
    }
    redirect(signedIn ? "/dashboard" : "/resources");
  }

  return <GetStartedWizard initialPrefs={prefs} editMode={editMode} />;
}
