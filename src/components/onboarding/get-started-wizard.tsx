"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dropdown } from "@/components/ui/dropdown";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";
import {
  MAX_PRIORITY_CATEGORIES,
  ONBOARDING_PRIORITY_SLUGS,
  SUPPORTED_ONBOARDING_STATES,
  getCountiesForState,
  readClientPreferences,
  type UserPreferences,
} from "@/lib/user-preferences";
import { saveUserPreferences } from "@/lib/user-preferences/save";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { cn, pageSectionPadding } from "@/lib/utils";

interface GetStartedWizardProps {
  initialPrefs: UserPreferences | null;
  editMode?: boolean;
}

export function GetStartedWizard({ initialPrefs, editMode = false }: GetStartedWizardProps) {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const { t } = useTranslations();

  const existing = initialPrefs ?? readClientPreferences();

  const [step, setStep] = useState(1);
  const [state, setState] = useState(existing?.state ?? "");
  const [county, setCounty] = useState(existing?.county ?? "");
  const [priorities, setPriorities] = useState<string[]>(existing?.priorityCategories ?? []);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const stateOptions = useMemo(
    () =>
      SUPPORTED_ONBOARDING_STATES.map((value) => ({
        value,
        label: t(`onboarding.states.${value === "Kentucky" ? "kentucky" : "ohio"}`),
      })),
    [t]
  );

  const countyOptions = useMemo(
    () =>
      getCountiesForState(state).map((value) => ({
        value,
        label: value,
      })),
    [state]
  );

  const togglePriority = (slug: string) => {
    setPriorities((current) => {
      if (current.includes(slug)) {
        return current.filter((item) => item !== slug);
      }
      if (current.length >= MAX_PRIORITY_CATEGORIES) {
        return current;
      }
      return [...current, slug];
    });
  };

  const handleStateChange = (value: string) => {
    setState(value);
    setCounty("");
  };

  const handleSkip = async () => {
    setSaving(true);
    setError(null);
    const result = await saveUserPreferences({ state: "", county: "", priorityCategories: [], skipped: true }, user?.id);
    setSaving(false);
    if (result.error) {
      setError(t("onboarding.saveFailed"));
      return;
    }
    router.push("/resources");
    router.refresh();
  };

  const handleSave = async () => {
    if (authLoading) return;

    setSaving(true);
    setError(null);
    const result = await saveUserPreferences(
      { state, county, priorityCategories: priorities },
      user?.id
    );
    setSaving(false);
    if (result.error || !result.prefs) {
      setError(t("onboarding.saveFailed"));
      return;
    }
    router.push(buildResourcesPageHref({ state, county }, "recommended"));
    router.refresh();
  };

  const canContinueStep1 = Boolean(state);
  const canContinueStep2 = Boolean(state && county);
  const canFinish = Boolean(state && county && priorities.length > 0) && !authLoading;

  return (
    <div className={pageSectionPadding}>
      <div className="mx-auto max-w-2xl">
        <header className="mb-8 text-center">
          <h1 className="mb-3 text-3xl font-bold sm:text-4xl">
            {editMode ? t("onboarding.editTitle") : t("onboarding.title")}
          </h1>
          <p className="text-lg text-muted-foreground">{t("onboarding.subtitle")}</p>
          <p className="mt-4 text-sm font-medium text-muted-foreground" aria-live="polite">
            {t("onboarding.stepIndicator", { current: step, total: 3 })}
          </p>
        </header>

        <Card className="space-y-6">
          {step === 1 && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold">{t("onboarding.stepStateTitle")}</h2>
              <p className="text-base text-muted-foreground">{t("onboarding.stepStateDesc")}</p>
              <Dropdown
                label={t("onboarding.stateLabel")}
                placeholder={t("onboarding.statePlaceholder")}
                value={state}
                options={stateOptions}
                onChange={handleStateChange}
              />
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold">{t("onboarding.stepCountyTitle")}</h2>
              <p className="text-base text-muted-foreground">{t("onboarding.stepCountyDesc")}</p>
              <Dropdown
                label={t("onboarding.countyLabel")}
                placeholder={t("onboarding.countyPlaceholder")}
                value={county}
                options={countyOptions}
                onChange={setCounty}
                searchable
                searchPlaceholder={t("onboarding.countySearchPlaceholder")}
                noResultsText={t("onboarding.countyNoResults")}
                disabled={!state}
              />
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold">{t("onboarding.stepPrioritiesTitle")}</h2>
              <p className="text-base text-muted-foreground">
                {t("onboarding.stepPrioritiesDesc", { max: MAX_PRIORITY_CATEGORIES })}
              </p>
              <div className="flex flex-wrap gap-2" role="group" aria-label={t("onboarding.stepPrioritiesTitle")}>
                {ONBOARDING_PRIORITY_SLUGS.map((slug) => {
                  const selected = priorities.includes(slug);
                  const maxReached = !selected && priorities.length >= MAX_PRIORITY_CATEGORIES;
                  return (
                    <button
                      key={slug}
                      type="button"
                      aria-pressed={selected}
                      disabled={maxReached}
                      onClick={() => togglePriority(slug)}
                      className={cn(
                        "inline-flex min-h-[48px] cursor-pointer items-center gap-2 rounded-xl border-2 px-4 py-2 text-base font-semibold transition-colors",
                        "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
                        selected
                          ? "border-primary bg-primary/10 text-primary"
                          : "border-border bg-card text-foreground hover:border-primary/40",
                        maxReached && "cursor-not-allowed opacity-50"
                      )}
                    >
                      {selected ? <Check className="h-4 w-4" aria-hidden="true" /> : null}
                      {t(`onboarding.priorities.${slug}`)}
                    </button>
                  );
                })}
              </div>
              <p className="text-sm text-muted-foreground">
                {t("onboarding.prioritiesSelected", { count: priorities.length, max: MAX_PRIORITY_CATEGORIES })}
              </p>
              <p className="text-sm">
                <Link
                  href={buildResourcesPageHref(
                    state && county ? { state, county } : undefined
                  )}
                  className="font-semibold text-primary hover:underline"
                >
                  {t("onboarding.browseAllCategories")}
                </Link>
              </p>
            </div>
          )}

          {error ? (
            <p role="alert" className="text-base text-destructive">
              {error}
            </p>
          ) : null}

          <div className="flex flex-col-reverse gap-3 border-t border-border pt-6 sm:flex-row sm:items-center sm:justify-between">
            <Button type="button" variant="ghost" onClick={handleSkip} loading={saving}>
              {t("onboarding.skip")}
            </Button>
            <div className="flex flex-col-reverse gap-2 sm:flex-row">
              {step > 1 ? (
                <Button type="button" variant="outline" onClick={() => setStep((s) => s - 1)} disabled={saving}>
                  {t("onboarding.back")}
                </Button>
              ) : null}
              {step < 3 ? (
                <Button
                  type="button"
                  onClick={() => setStep((s) => s + 1)}
                  loading={saving}
                  disabled={
                    (step === 1 && !canContinueStep1) || (step === 2 && !canContinueStep2)
                  }
                >
                  {t("onboarding.continue")}
                </Button>
              ) : (
                <Button type="button" onClick={handleSave} loading={saving} disabled={!canFinish}>
                  {saving ? t("onboarding.saving") : t("onboarding.finish")}
                </Button>
              )}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
