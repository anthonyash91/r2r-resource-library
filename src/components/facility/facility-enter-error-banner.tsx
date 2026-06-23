import Link from "next/link";
import { getServerTranslator } from "@/i18n/server";

export async function FacilityEnterErrorBanner({ error }: { error?: string }) {
  if (!error) return null;

  const { t } = await getServerTranslator();
  const messageKey =
    error === "unconfigured"
      ? "facility.enterErrorUnconfigured"
      : error === "config"
        ? "facility.enterErrorConfig"
        : "facility.enterErrorInvalid";

  return (
    <div
      role="alert"
      className="border-b border-destructive/30 bg-destructive/10 px-4 py-4 text-center text-base text-destructive"
    >
      <p className="font-semibold">{t("facility.enterErrorTitle")}</p>
      <p className="mt-1 text-destructive/90">{t(messageKey)}</p>
      {error === "invalid" ? (
        <p className="mt-2">
          <Link href="/admin/facilities" className="font-semibold underline hover:no-underline">
            {t("facility.enterErrorAdminLink")}
          </Link>
        </p>
      ) : null}
    </div>
  );
}
