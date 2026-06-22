import { createCipheriv, createDecipheriv, createHash, createHmac, randomBytes } from "crypto";

const ALGORITHM = "aes-256-gcm";
const IV_LENGTH = 12;

function getSecret(): string {
  const secret = process.env.FACILITY_CRYPTO_SECRET?.trim();
  if (!secret) {
    if (process.env.NODE_ENV === "production") {
      throw new Error("FACILITY_CRYPTO_SECRET is not configured");
    }
    return "dev-facility-crypto-secret-change-me";
  }
  return secret;
}

function getEncryptionKey(): Buffer {
  return createHash("sha256").update(getSecret()).digest();
}

export function normalizeSiteId(siteId: string): string {
  return siteId.trim().toUpperCase();
}

export function normalizePin(pin: string): string {
  return pin.trim();
}

export function normalizeRecoveryAnswer(answer: string): string {
  return answer.trim().toLowerCase().replace(/\s+/g, " ");
}

export function hashSiteId(siteId: string): string {
  return createHmac("sha256", getSecret())
    .update(`site:${normalizeSiteId(siteId)}`)
    .digest("hex");
}

export function hashInmatePin(facilityId: string, pin: string): string {
  return createHmac("sha256", getSecret())
    .update(`pin:${facilityId}:${normalizePin(pin)}`)
    .digest("hex");
}

export function hashRecoveryAnswer(answer: string): string {
  return createHmac("sha256", getSecret())
    .update(`recovery:${normalizeRecoveryAnswer(answer)}`)
    .digest("hex");
}

export function encryptSiteId(siteId: string): string {
  const iv = randomBytes(IV_LENGTH);
  const cipher = createCipheriv(ALGORITHM, getEncryptionKey(), iv);
  const encrypted = Buffer.concat([
    cipher.update(normalizeSiteId(siteId), "utf8"),
    cipher.final(),
  ]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]).toString("base64url");
}

export function decryptSiteId(payload: string): string {
  const buffer = Buffer.from(payload, "base64url");
  const iv = buffer.subarray(0, IV_LENGTH);
  const tag = buffer.subarray(IV_LENGTH, IV_LENGTH + 16);
  const encrypted = buffer.subarray(IV_LENGTH + 16);
  const decipher = createDecipheriv(ALGORITHM, getEncryptionKey(), iv);
  decipher.setAuthTag(tag);
  const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
  return decrypted.toString("utf8");
}

export function encryptFacilitySessionPayload(payload: string): string {
  const iv = randomBytes(IV_LENGTH);
  const cipher = createCipheriv(ALGORITHM, getEncryptionKey(), iv);
  const encrypted = Buffer.concat([cipher.update(payload, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]).toString("base64url");
}

export function decryptFacilitySessionPayload(payload: string): string | null {
  try {
    const buffer = Buffer.from(payload, "base64url");
    const iv = buffer.subarray(0, IV_LENGTH);
    const tag = buffer.subarray(IV_LENGTH, IV_LENGTH + 16);
    const encrypted = buffer.subarray(IV_LENGTH + 16);
    const decipher = createDecipheriv(ALGORITHM, getEncryptionKey(), iv);
    decipher.setAuthTag(tag);
    const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
    return decrypted.toString("utf8");
  } catch {
    return null;
  }
}

export function maskSiteId(siteId: string): string {
  const normalized = normalizeSiteId(siteId);
  if (normalized.length <= 4) return "••••";
  return `••••${normalized.slice(-4)}`;
}
