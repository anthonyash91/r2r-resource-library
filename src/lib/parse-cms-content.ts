export type CmsContentBlock =
  | { type: "paragraph"; text: string }
  | { type: "section"; title: string; body?: string; items?: string[] };

function isBulletLine(line: string): boolean {
  return /^[•\-*]\s/.test(line);
}

function stripBullet(line: string): string {
  return line.replace(/^[•\-*]\s*/, "").trim();
}

function looksLikeHeading(line: string): boolean {
  return line.length <= 80 && !line.endsWith(".") && !line.endsWith("?");
}

export function parseCmsContent(content: string): CmsContentBlock[] {
  const chunks = content.trim().split(/\n\n+/).map((chunk) => chunk.trim()).filter(Boolean);
  const blocks: CmsContentBlock[] = [];

  for (const chunk of chunks) {
    const lines = chunk.split("\n").map((line) => line.trim()).filter(Boolean);
    if (lines.length === 0) continue;

    const bulletLines = lines.filter(isBulletLine);
    const textLines = lines.filter((line) => !isBulletLine(line));

    if (bulletLines.length > 0) {
      if (textLines.length === 1 && looksLikeHeading(textLines[0])) {
        blocks.push({
          type: "section",
          title: textLines[0],
          items: bulletLines.map(stripBullet),
        });
        continue;
      }

      if (textLines.length > 0) {
        blocks.push({ type: "paragraph", text: textLines.join("\n\n") });
      }

      blocks.push({
        type: "section",
        title: "",
        items: bulletLines.map(stripBullet),
      });
      continue;
    }

    if (textLines.length >= 2 && looksLikeHeading(textLines[0])) {
      blocks.push({
        type: "section",
        title: textLines[0],
        body: textLines.slice(1).join("\n\n"),
      });
      continue;
    }

    blocks.push({ type: "paragraph", text: textLines.join("\n\n") });
  }

  return blocks;
}
