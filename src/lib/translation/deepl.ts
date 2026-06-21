const DEEPL_FREE_API = "https://api-free.deepl.com/v2/translate";
const DEEPL_PRO_API = "https://api.deepl.com/v2/translate";

export function isTranslationConfigured(): boolean {
  return Boolean(process.env.DEEPL_API_KEY?.trim());
}

function getDeepLApiUrl(apiKey: string): string {
  return apiKey.endsWith(":fx") ? DEEPL_FREE_API : DEEPL_PRO_API;
}

type DeepLTranslationResponse = {
  translations: { detected_source_language: string; text: string }[];
};

export async function translateTextsToSpanish(texts: string[]): Promise<string[]> {
  const apiKey = process.env.DEEPL_API_KEY?.trim();
  if (!apiKey) {
    throw new Error("TRANSLATION_NOT_CONFIGURED");
  }

  const trimmed = texts.map((text) => text.trim());
  const results = trimmed.map(() => "");
  const batchIndices: number[] = [];

  for (let i = 0; i < trimmed.length; i++) {
    if (trimmed[i]) batchIndices.push(i);
  }

  if (batchIndices.length === 0) return results;

  const response = await fetch(getDeepLApiUrl(apiKey), {
    method: "POST",
    headers: {
      Authorization: `DeepL-Auth-Key ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: batchIndices.map((index) => trimmed[index]),
      source_lang: "EN",
      target_lang: "ES",
    }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`DeepL request failed (${response.status}): ${detail}`);
  }

  const data = (await response.json()) as DeepLTranslationResponse;

  batchIndices.forEach((sourceIndex, batchIndex) => {
    results[sourceIndex] = data.translations[batchIndex]?.text ?? trimmed[sourceIndex];
  });

  return results;
}

export async function translateTextToSpanish(text: string): Promise<string> {
  const [translated] = await translateTextsToSpanish([text]);
  return translated;
}
