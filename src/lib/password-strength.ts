export type PasswordStrengthLevel = 0 | 1 | 2 | 3 | 4;

export function scorePassword(password: string): PasswordStrengthLevel {
  if (!password) return 0;
  if (password.length < 8) return 1;

  let variety = 0;
  if (/[a-z]/.test(password)) variety++;
  if (/[A-Z]/.test(password)) variety++;
  if (/\d/.test(password)) variety++;
  if (/[^a-zA-Z0-9]/.test(password)) variety++;

  if (password.length >= 12 && variety >= 3) return 4;
  if (variety >= 3) return 3;
  if (variety >= 2) return 2;
  return 1;
}
