"use client";

import Link from "next/link";
import { DoorOpen, FileInput, Info, ShieldCheck } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import {
  intakeBadgeWalkInClass,
  intakeBadgeWalkInSmClass,
  intakeBadgeSuccessClass,
  intakeBadgeSuccessSmClass,
  intakeBadgeWarningClass,
  intakeBadgeWarningSmClass,
} from "@/components/layout/site-branding-styles";
import { buildResourcesPageHref } from "@/lib/resources-page";
import {
  getResourceIntakeSignals,
  serializeIntakeFilterParam,
  type IntakeSignal,
} from "@/lib/intake-signals";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";
import type { Resource } from "@/types";

const SIGNAL_META: Record<
  IntakeSignal,
  { icon: LucideIcon; className: string; smClassName: string }
> = {
  accepts_criminal_record: {
    icon: ShieldCheck,
    className: intakeBadgeSuccessClass,
    smClassName: intakeBadgeSuccessSmClass,
  },
  referral_required: {
    icon: FileInput,
    className: intakeBadgeWarningClass,
    smClassName: intakeBadgeWarningSmClass,
  },
  walk_in_ok: {
    icon: DoorOpen,
    className: intakeBadgeWalkInClass,
    smClassName: intakeBadgeWalkInSmClass,
  },
};

interface IntakeSignalMetaProps {
  resource: Pick<Resource, "intake_signals">;
  compact?: boolean;
  className?: string;
}

/** Card footer line: info icon + linked intake labels for filtering. */
export function IntakeSignalMeta({ resource, compact = false, className }: IntakeSignalMetaProps) {
  const { t } = useTranslations();
  const signals = getResourceIntakeSignals(resource);

  if (signals.length === 0) return null;

  const labels = signals.map((signal) => t(`resources.intakeSignals.${signal}`));

  return (
    <p
      className={cn("flex min-w-0 items-start gap-2", className)}
      aria-label={t("resources.intakeMetaAria", { labels: labels.join(", ") })}
    >
      <Info
        className={cn("mt-0.5 shrink-0 text-primary", compact ? "h-3.5 w-3.5" : "h-4 w-4")}
        aria-hidden="true"
      />
      <span className="min-w-0 break-words">
        {signals.map((signal, index) => {
          const label = t(`resources.intakeSignals.${signal}`);
          return (
            <span key={signal}>
              {index > 0 ? <span aria-hidden="true">, </span> : null}
              <Link
                href={buildResourcesPageHref(
                  { intake: serializeIntakeFilterParam([signal]) },
                  "results"
                )}
                className="text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                aria-label={t("resources.intakeSignalFilterAria", { label })}
              >
                {label}
              </Link>
            </span>
          );
        })}
      </span>
    </p>
  );
}

interface IntakeSignalBadgesProps {
  resource: Pick<Resource, "intake_signals">;
  size?: "default" | "sm";
  linkable?: boolean;
  className?: string;
}

export function IntakeSignalBadges({
  resource,
  size = "default",
  linkable = true,
  className,
}: IntakeSignalBadgesProps) {
  const { t } = useTranslations();
  const signals = getResourceIntakeSignals(resource);

  if (signals.length === 0) return null;

  const isSmall = size === "sm";

  return (
    <div className={cn("flex flex-wrap gap-2", className)}>
      {signals.map((signal) => {
        const { icon: Icon, className: badgeClass, smClassName } = SIGNAL_META[signal];
        const label = t(`resources.intakeSignals.${signal}`);
        const badgeClassName = cn(
          isSmall ? smClassName : badgeClass,
          "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
        );

        const content = (
          <>
            <Icon aria-hidden="true" />
            {label}
          </>
        );

        if (!linkable) {
          return (
            <span key={signal} className={badgeClassName}>
              {content}
            </span>
          );
        }

        return (
          <Link
            key={signal}
            href={buildResourcesPageHref(
              { intake: serializeIntakeFilterParam([signal]) },
              "results"
            )}
            className={badgeClassName}
            aria-label={t("resources.intakeSignalFilterAria", { label })}
          >
            {content}
          </Link>
        );
      })}
    </div>
  );
}
