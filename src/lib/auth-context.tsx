"use client";

import { createContext, useContext, useEffect, useState, useCallback } from "react";
import type { Profile } from "@/types";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { MOCK_ADMIN_USER } from "@/lib/mock-data";
import { createTranslator } from "@/i18n/translator";
import { DEFAULT_LOCALE, LOCALE_COOKIE, type Locale } from "@/i18n/types";

interface AuthContextType {
  user: Profile | null;
  loading: boolean;
  isAdmin: boolean;
  signIn: (email: string, password: string) => Promise<{ error?: string }>;
  signUp: (email: string, password: string, fullName: string) => Promise<{ error?: string }>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const DEMO_USER_KEY = "reentry_demo_user";

function getClientLocale(): Locale {
  if (typeof document === "undefined") return DEFAULT_LOCALE;
  const match = document.cookie.match(new RegExp(`(?:^|; )${LOCALE_COOKIE}=([^;]*)`));
  return match?.[1] === "es" ? "es" : DEFAULT_LOCALE;
}

function authUnavailableMessage() {
  return createTranslator(getClientLocale()).t("auth.authUnavailable");
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  const loadDemoUser = useCallback(() => {
    if (typeof window === "undefined") return;
    const stored = localStorage.getItem(DEMO_USER_KEY);
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch {
        localStorage.removeItem(DEMO_USER_KEY);
      }
    }
  }, []);

  useEffect(() => {
    if (!isSupabaseConfigured()) {
      loadDemoUser();
      setLoading(false);
      return;
    }

    const supabase = createClient();
    if (!supabase) {
      loadDemoUser();
      setLoading(false);
      return;
    }

    const fetchProfile = async (userId: string) => {
      const { data } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", userId)
        .single();
      if (data) setUser(data as Profile);
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
  }, [loadDemoUser]);

  const signIn = async (email: string, password: string) => {
    if (!isSupabaseConfigured()) {
      const demoUser: Profile = email.includes("admin")
        ? MOCK_ADMIN_USER
        : {
            id: "demo-user",
            email,
            full_name: email.split("@")[0],
            role: "user",
            is_active: true,
            phone: null,
            state: null,
            county: null,
            city: null,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          };
      localStorage.setItem(DEMO_USER_KEY, JSON.stringify(demoUser));
      setUser(demoUser);
      return {};
    }

    const supabase = createClient();
    if (!supabase) return { error: authUnavailableMessage() };

    const { error } = await supabase.auth.signInWithPassword({ email, password });
    return error ? { error: error.message } : {};
  };

  const signUp = async (email: string, password: string, fullName: string) => {
    if (!isSupabaseConfigured()) {
      const demoUser: Profile = {
        id: "demo-user",
        email,
        full_name: fullName,
        role: "user",
        is_active: true,
        phone: null,
        state: null,
        county: null,
        city: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      localStorage.setItem(DEMO_USER_KEY, JSON.stringify(demoUser));
      setUser(demoUser);
      return {};
    }

    const supabase = createClient();
    if (!supabase) return { error: authUnavailableMessage() };

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { data: { full_name: fullName } },
    });
    return error ? { error: error.message } : {};
  };

  const signOut = async () => {
    if (!isSupabaseConfigured()) {
      localStorage.removeItem(DEMO_USER_KEY);
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
