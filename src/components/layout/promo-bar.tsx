import { getServerTranslator } from "@/i18n/server";

export async function PromoBar() {
  const { t } = await getServerTranslator();

  return (
    <div className="app-promo-bar text-center text-[13px] font-semibold tracking-wide text-white sm:text-sm">
      <p className="mx-auto max-w-[1180px] px-4 py-[15px] sm:px-9">
        {t("promoBar.message")}{" "}
        <strong className="font-bold">{t("promoBar.crisisNumber")}</strong>
      </p>
    </div>
  );
}
