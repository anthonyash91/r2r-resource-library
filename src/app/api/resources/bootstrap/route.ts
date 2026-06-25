import { NextResponse } from "next/server";
import {
  getResourcesBootstrap,
  resolveEffectiveResourcesPageParams,
} from "@/lib/resources-bootstrap";
import { getServerUserPreferences } from "@/lib/user-preferences/server";
import {
  resourcesPageParamsFromSearchParams,
} from "@/lib/resources-page-filters";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const urlParams = resourcesPageParamsFromSearchParams(searchParams);
  const preferences = await getServerUserPreferences();
  const params = resolveEffectiveResourcesPageParams(urlParams, preferences);
  const bootstrap = await getResourcesBootstrap(params);

  return NextResponse.json(bootstrap);
}
