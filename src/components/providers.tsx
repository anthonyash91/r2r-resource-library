"use client";

import { AuthProvider } from "@/lib/auth-context";
import { SavedProvider } from "@/lib/saved-context";
import { BreadcrumbProvider } from "@/lib/breadcrumb-context";
import { LocaleProvider } from "@/i18n/locale-context";
import { FacilityInactivityGuard } from "@/components/facility/facility-inactivity-guard";
import { FacilityTabletHandoff } from "@/components/facility/facility-tablet-handoff";
import { FacilityPinGuard } from "@/components/facility/facility-pin-guard";
import { FacilitySessionPreferencesHydration } from "@/components/facility/facility-session-preferences-hydration";
import type { Locale } from "@/i18n/types";

export function Providers({
  children,
  initialLocale,
}: {
  children: React.ReactNode;
  initialLocale?: Locale;
}) {
  return (
    <LocaleProvider initialLocale={initialLocale}>
      <BreadcrumbProvider>
        <AuthProvider>
          <FacilityTabletHandoff />
          <FacilityPinGuard />
          <FacilitySessionPreferencesHydration />
          <FacilityInactivityGuard>
            <SavedProvider>{children}</SavedProvider>
          </FacilityInactivityGuard>
        </AuthProvider>
      </BreadcrumbProvider>
    </LocaleProvider>
  );
}
