"use client";

import { createContext, useContext, useEffect, useState, useCallback } from "react";
import type { Resource } from "@/types";
import { useAuth } from "@/lib/auth-context";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import { MOCK_RESOURCES } from "@/lib/mock-data";

interface SavedContextType {
  savedIds: Set<string>;
  recentlyViewed: Resource[];
  toggleSave: (resourceId: string) => Promise<void>;
  isSaved: (resourceId: string) => boolean;
  recordView: (resource: Resource) => void;
  loading: boolean;
}

const SavedContext = createContext<SavedContextType | undefined>(undefined);

const SAVED_KEY = "reentry_saved_resources";
const VIEWED_KEY = "reentry_recently_viewed";

export function SavedProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());
  const [recentlyViewed, setRecentlyViewed] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);

  const loadLocal = useCallback(() => {
    if (typeof window === "undefined") return;
    const saved = localStorage.getItem(SAVED_KEY);
    if (saved) {
      try {
        setSavedIds(new Set(JSON.parse(saved)));
      } catch {
        localStorage.removeItem(SAVED_KEY);
      }
    }
    const viewed = localStorage.getItem(VIEWED_KEY);
    if (viewed) {
      try {
        setRecentlyViewed(JSON.parse(viewed));
      } catch {
        localStorage.removeItem(VIEWED_KEY);
      }
    }
  }, []);

  const persistSaved = (ids: Set<string>) => {
    localStorage.setItem(SAVED_KEY, JSON.stringify([...ids]));
  };

  const persistViewed = (resources: Resource[]) => {
    localStorage.setItem(VIEWED_KEY, JSON.stringify(resources.slice(0, 10)));
  };

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

    const supabase = createClient();
    if (!supabase) {
      loadLocal();
      setLoading(false);
      return;
    }

    const fetchSaved = async () => {
      const { data } = await supabase
        .from("saved_resources")
        .select("resource_id")
        .eq("user_id", user.id);

      if (data) {
        setSavedIds(new Set(data.map((s) => s.resource_id)));
      }
      setLoading(false);
    };

    fetchSaved();
  }, [user, loadLocal]);

  const toggleSave = async (resourceId: string) => {
    const next = new Set(savedIds);
    const wasSaved = next.has(resourceId);

    if (wasSaved) {
      next.delete(resourceId);
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
      await supabase
        .from("saved_resources")
        .insert({ user_id: user.id, resource_id: resourceId });
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

    if (user && isSupabaseConfigured()) {
      const supabase = createClient();
      supabase?.from("resource_views").insert({
        user_id: user.id,
        resource_id: resource.id,
      });
    }
  }, [user]);

  const getSavedResources = (): Resource[] => {
    return MOCK_RESOURCES.filter((r) => savedIds.has(r.id));
  };

  return (
    <SavedContext.Provider
      value={{
        savedIds,
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
  const { savedIds } = useSaved();
  return MOCK_RESOURCES.filter((r) => savedIds.has(r.id));
}
