"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useMemo,
} from "react";
import type { Resource } from "@/types";
import { useAuth } from "@/lib/auth-context";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { MOCK_RESOURCES } from "@/lib/mock-data";
import {
  clearViewLoggedThisSession,
  getOrCreateSessionId,
  hasLoggedViewThisSession,
  markViewLoggedThisSession,
} from "@/lib/view-tracking";
import { useTranslations } from "@/i18n/locale-context";
import { localizeResources } from "@/i18n/localize-content";

interface SavedContextType {
  savedIds: Set<string>;
  savedResources: Resource[];
  recentlyViewed: Resource[];
  toggleSave: (resourceId: string) => Promise<void>;
  isSaved: (resourceId: string) => boolean;
  recordView: (resource: Resource) => void;
  loading: boolean;
}

const SavedContext = createContext<SavedContextType | undefined>(undefined);

const SAVED_KEY = "reentry_saved_resources";
const VIEWED_KEY = "reentry_recently_viewed";

type SavedRow = {
  resource_id: string;
  resource: Resource | null;
};

export function SavedProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const { locale } = useTranslations();
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());
  const [savedResourcesBase, setSavedResourcesBase] = useState<Resource[]>([]);
  const [recentlyViewed, setRecentlyViewed] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);

  const savedResources = useMemo(
    () => localizeResources(savedResourcesBase, locale),
    [savedResourcesBase, locale]
  );

  const syncMockSavedResources = useCallback((ids: Set<string>) => {
    setSavedResourcesBase(MOCK_RESOURCES.filter((r) => ids.has(r.id)));
  }, []);

  const loadLocal = useCallback(() => {
    if (typeof window === "undefined") return;
    const saved = localStorage.getItem(SAVED_KEY);
    if (saved) {
      try {
        const ids = new Set<string>(JSON.parse(saved));
        setSavedIds(ids);
        syncMockSavedResources(ids);
      } catch {
        localStorage.removeItem(SAVED_KEY);
      }
    } else {
      setSavedIds(new Set());
      setSavedResourcesBase([]);
    }
    const viewed = localStorage.getItem(VIEWED_KEY);
    if (viewed) {
      try {
        setRecentlyViewed(JSON.parse(viewed));
      } catch {
        localStorage.removeItem(VIEWED_KEY);
      }
    }
  }, [syncMockSavedResources]);

  const persistSaved = (ids: Set<string>) => {
    localStorage.setItem(SAVED_KEY, JSON.stringify([...ids]));
  };

  const persistViewed = (resources: Resource[]) => {
    localStorage.setItem(VIEWED_KEY, JSON.stringify(resources.slice(0, 10)));
  };

  const fetchSavedFromSupabase = useCallback(async (userId: string) => {
    const supabase = createClient();
    if (!supabase) {
      loadLocal();
      setLoading(false);
      return;
    }

    setLoading(true);
    const { data } = await supabase
      .from("saved_resources")
      .select("resource_id, resource:resources(*, category:categories(*))")
      .eq("user_id", userId)
      .order("created_at", { ascending: false });

    if (data) {
      const rows = data as unknown as SavedRow[];
      setSavedIds(new Set(rows.map((s) => s.resource_id)));
      setSavedResourcesBase(
        rows
          .map((row) => row.resource)
          .filter((resource): resource is Resource => resource != null)
      );
    }
    setLoading(false);
  }, [loadLocal]);

  useEffect(() => {
    if (!user) {
      loadLocal();
      setLoading(false);
      return;
    }

    if (!isSupabaseConfigured()) {
      loadLocal();
      setLoading(false);
      return;
    }

    fetchSavedFromSupabase(user.id);
  }, [user, loadLocal, fetchSavedFromSupabase]);

  const toggleSave = async (resourceId: string) => {
    const next = new Set(savedIds);
    const wasSaved = next.has(resourceId);

    if (wasSaved) {
      next.delete(resourceId);
      setSavedResourcesBase((prev) => prev.filter((r) => r.id !== resourceId));
    } else {
      next.add(resourceId);
    }
    setSavedIds(next);
    persistSaved(next);

    if (!user || !isSupabaseConfigured()) return;

    const supabase = createClient();
    if (!supabase) return;

    if (wasSaved) {
      await supabase
        .from("saved_resources")
        .delete()
        .eq("user_id", user.id)
        .eq("resource_id", resourceId);
    } else {
      const { error: insertError } = await supabase
        .from("saved_resources")
        .insert({ user_id: user.id, resource_id: resourceId });

      if (!insertError) {
        const { data } = await supabase
          .from("resources")
          .select("*, category:categories(*)")
          .eq("id", resourceId)
          .single();

        if (data) {
          setSavedResourcesBase((prev) => [data as Resource, ...prev]);
        }
      } else {
        await fetchSavedFromSupabase(user.id);
      }
    }
  };

  const isSaved = (resourceId: string) => savedIds.has(resourceId);

  const recordView = useCallback((resource: Resource) => {
    setRecentlyViewed((prev) => {
      const filtered = prev.filter((r) => r.id !== resource.id);
      const next = [resource, ...filtered].slice(0, 10);
      persistViewed(next);
      return next;
    });

    if (!isSupabaseConfigured() || hasLoggedViewThisSession(resource.id)) return;

    const supabase = createClient();
    if (!supabase) return;

    markViewLoggedThisSession(resource.id);

    const payload = {
      user_id: user?.id ?? null,
      resource_id: resource.id,
      session_id: user ? null : getOrCreateSessionId(),
    };

    void supabase.from("resource_views").insert(payload).then(({ error }) => {
      if (error) clearViewLoggedThisSession(resource.id);
    });
  }, [user]);

  return (
    <SavedContext.Provider
      value={{
        savedIds,
        savedResources,
        recentlyViewed,
        toggleSave,
        isSaved,
        recordView,
        loading,
      }}
    >
      {children}
    </SavedContext.Provider>
  );
}

export function useSaved() {
  const context = useContext(SavedContext);
  if (!context) throw new Error("useSaved must be used within SavedProvider");
  return context;
}

export function useSavedResources(): Resource[] {
  const { savedResources } = useSaved();
  return savedResources;
}
