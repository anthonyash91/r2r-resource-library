import { getHomepageContentAdmin, getAllResourcesAdmin } from "@/lib/data";
import { HomepageEditor } from "./homepage-editor";
import { getServerTranslator } from "@/i18n/server";
import type { SiteContentFormValues } from "@/lib/site-content-fields";

export default async function AdminHomepagePage() {
  const { t } = await getServerTranslator();
  const [content, resources] = await Promise.all([
    getHomepageContentAdmin(),
    getAllResourcesAdmin(),
  ]);

  const initial: SiteContentFormValues = {
    hero_headline: content.hero_headline || t("home.heroHeadline"),
    hero_subheadline: content.hero_subheadline || t("home.heroSubheadline"),
    hero_headline_highlight: content.hero_headline_highlight || t("home.heroHighlight"),
    nav_brand_name: content.nav_brand_name || t("nav.brandName"),
    nav_tagline: content.nav_tagline || t("nav.tagline"),
    footer_tagline: content.footer_tagline || t("footer.tagline"),
    footer_description: content.footer_description || t("footer.description"),
  };

  return <HomepageEditor initial={initial} resources={resources} />;
}
