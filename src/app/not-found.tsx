import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getServerTranslator } from "@/i18n/server";

export default async function NotFound() {
  const { t } = await getServerTranslator();

  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center px-4 text-center">
      <h1 className="mb-4 text-4xl font-bold">{t("notFound.title")}</h1>
      <p className="mb-8 text-lg text-muted-foreground">{t("notFound.message")}</p>
      <Link href="/">
        <Button size="lg">{t("notFound.goHome")}</Button>
      </Link>
    </div>
  );
}
