"use client";

import { createContext, useContext, useEffect, useState, useCallback } from "react";
import type { Profile } from "@/types";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { formatAuthError, isProfileSetupError } from "@/lib/auth-errors";
import { writeClientPreferences } from "@/lib/user-preferences/client";
import {
  hasCompletedOnboarding,
  preferencesFromProfile,
} from "@/lib/user-preferences/parse";
import { syncCookiePreferencesToProfile } from "@/lib/user-preferences/sync-profile";
import { createTranslator } from "@/i18n/translator";
import { DEFAULT_LOCALE, LOCALE_COOKIE, type Locale } from "@/i18n/types";

interface AuthContextType {
  user: Profile | null;
  loading: boolean;
  isAdmin: boolean;
  signIn: (email: string, password: string) => Promise<{ error?: string; isAdmin?: boolean }>;
  signUp: (
    email: string,
    password: string,
    fullName: string
  ) => Promise<{ error?: string; needsEmailConfirmation?: boolean }>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function getClientLocale(): Locale {
  if (typeof document === "undefined") return DEFAULT_LOCALE;
  const match = document.cookie.match(new RegExp(`(?:^|; )${LOCALE_COOKIE}=([^;]*)`));
  return match?.[1] === "es" ? "es" : DEFAULT_LOCALE;
}

function authMessage(
  key:
    | "authUnavailable"
    | "signInFailed"
    | "signUpFailed"
    | "signUpDatabaseError"
) {
  return createTranslator(getClientLocale()).t(`auth.${key}`);
}

function facilityMessage(key: "pinMismatch") {
  return createTranslator(getClientLocale()).t(`facility.${key}`);
}

async function verifyFacilityLoginAfterAuth(
  supabase: NonNullable<ReturnType<typeof createClient>>
): Promise<string | undefined> {
  const response = await fetch("/api/facility/verify-login");
  if (response.status === 403) {
    await supabase.auth.signOut();
    return facilityMessage("pinMismatch");
  }
  return undefined;
}

function getAuthRedirectUrl() {
  if (typeof window !== "undefined") return window.location.origin;
  return process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:8080";
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isSupabaseConfigured()) {
      setLoading(false);
      return;
    }

    const supabase = createClient();
    if (!supabase) {
      setLoading(false);
      return;
    }

    const fetchProfile = async (userId: string) => {
      const { data } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", userId)
        .single();
      if (data) {
        const profile = data as Profile;
        setUser(profile);
        await syncCookiePreferencesToProfile(userId);
        const profilePrefs = preferencesFromProfile(profile);
        if (hasCompletedOnboarding(profilePrefs)) {
          writeClientPreferences(profilePrefs);
        }
      }
    };

    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session?.user) fetchProfile(session.user.id);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        if (session?.user) {
          fetchProfile(session.user.id);
        } else {
          setUser(null);
        }
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signIn = async (email: string, password: string) => {
    if (!isSupabaseConfigured()) {
      return { error: authMessage("authUnavailable") };
    }

    const supabase = createClient();
    if (!supabase) return { error: authMessage("authUnavailable") };

    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      const message = formatAuthError(error, authMessage("signInFailed"));
      return { error: message };
    }

    const userId = data.user?.id;
    if (!userId) {
      return { error: authMessage("signInFailed") };
    }

    const facilityError = await verifyFacilityLoginAfterAuth(supabase);
    if (facilityError) {
      setUser(null);
      return { error: facilityError };
    }

    const { data: profile } = await supabase
      .from("profiles")
      .select("*")
      .eq("id", userId)
      .single();

    if (profile) {
      const typedProfile = profile as Profile;
      setUser(typedProfile);
      const profilePrefs = preferencesFromProfile(typedProfile);
      if (hasCompletedOnboarding(profilePrefs)) {
        writeClientPreferences(profilePrefs);
      }
      await syncCookiePreferencesToProfile(userId);
      return { isAdmin: typedProfile.role === "admin" };
    }

    return { isAdmin: false };
  };

  const signUp = async (email: string, password: string, fullName: string) => {
    if (!isSupabaseConfigured()) {
      return { error: authMessage("authUnavailable") };
    }

    const supabase = createClient();
    if (!supabase) return { error: authMessage("authUnavailable") };

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { full_name: fullName },
        emailRedirectTo: `${getAuthRedirectUrl()}/auth/callback?next=/dashboard`,
      },
    });

    if (error) {
      const message = formatAuthError(error, authMessage("signUpFailed"));
      if (isProfileSetupError(message)) {
        return { error: authMessage("signUpDatabaseError") };
      }
      return { error: message };
    }

    if (!data.session) {
      return { needsEmailConfirmation: true };
    }

    if (data.user?.id) {
      await supabase
        .from("profiles")
        .update({ signup_context: "standard" })
        .eq("id", data.user.id);
      await syncCookiePreferencesToProfile(data.user.id);
    }

    return {};
  };

  const signOut = async () => {
    if (!isSupabaseConfigured()) {
      setUser(null);
      return;
    }

    const supabase = createClient();
    if (supabase) await supabase.auth.signOut();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAdmin: user?.role === "admin",
        signIn,
        signUp,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
