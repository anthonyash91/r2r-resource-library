import {
  createCipheriv,
  createDecipheriv,
  createHash,
  createHmac,
  randomBytes,
  timingSafeEqual,
} from "crypto";

const ALGORITHM = "aes-256-gcm";
const IV_LENGTH = 12;
export const DEV_FACILITY_CRYPTO_SECRET = "dev-facility-crypto-secret-change-me";

function getSecret(): string {
  const secret = process.env.FACILITY_CRYPTO_SECRET?.trim();
  if (secret) return secret;
  if (process.env.NODE_ENV === "production") {
    throw new Error("FACILITY_CRYPTO_SECRET is not configured");
  }
  if (process.env.ALLOW_DEV_FACILITY_CRYPTO === "1") {
    return DEV_FACILITY_CRYPTO_SECRET;
  }
  throw new Error(
    "FACILITY_CRYPTO_SECRET is not configured (set ALLOW_DEV_FACILITY_CRYPTO=1 for local dev only)"
  );
}

/** Constant-time compare for fixed-length hex digests (e.g. SHA-256 HMAC). */
export function secureCompareHex(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  try {
    return timingSafeEqual(Buffer.from(a, "hex"), Buffer.from(b, "hex"));
  } catch {
    return false;
  }
}

function getEncryptionKey(): Buffer {
  return encryptionKeyFromSecret(getSecret());
}

function encryptionKeyFromSecret(secret: string): Buffer {
  return createHash("sha256").update(secret).digest();
}

export function normalizeSiteId(siteId: string): string {
  return siteId.trim().toUpperCase();
}

export function normalizePin(pin: string): string {
  return pin.trim();
}

export function maskPin(pin: string): string {
  const normalized = normalizePin(pin);
  return normalized ? "*".repeat(normalized.length) : "";
}

export function normalizeRecoveryAnswer(answer: string): string {
  return answer.trim().toLowerCase().replace(/\s+/g, " ");
}

export function hashSiteId(siteId: string): string {
  return hashSiteIdWithSecret(siteId, getSecret());
}

export function hashSiteIdWithSecret(siteId: string, secret: string): string {
  return createHmac("sha256", secret)
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
  const decrypted = tryDecryptSiteId(payload);
  if (decrypted === null) {
    throw new Error("Failed to decrypt facility site ID");
  }
  return decrypted;
}

export function tryDecryptSiteId(payload: string): string | null {
  return tryDecryptSiteIdWithSecret(payload, getSecret());
}

export function tryDecryptSiteIdWithSecret(payload: string, secret: string): string | null {
  try {
    const buffer = Buffer.from(payload, "base64url");
    const iv = buffer.subarray(0, IV_LENGTH);
    const tag = buffer.subarray(IV_LENGTH, IV_LENGTH + 16);
    const encrypted = buffer.subarray(IV_LENGTH + 16);
    const decipher = createDecipheriv(ALGORITHM, encryptionKeyFromSecret(secret), iv);
    decipher.setAuthTag(tag);
    const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
    return decrypted.toString("utf8");
  } catch {
    return null;
  }
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
