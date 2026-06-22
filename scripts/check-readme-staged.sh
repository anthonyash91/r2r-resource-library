#!/usr/bin/env bash
# Remind contributors to update README.md when product-facing files change.
# Set SKIP_README_HOOK=1 to bypass, or use: git commit --no-verify

set -euo pipefail

if [[ "${SKIP_README_HOOK:-}" == "1" ]]; then
  exit 0
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  exit 0
fi

STAGED="$(git diff --cached --name-only)"
if [[ -z "$STAGED" ]]; then
  exit 0
fi

needs_readme_update=false

while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  case "$file" in
    README.md|package-lock.json|pnpm-lock.yaml|yarn.lock)
      continue
      ;;
    src/*|supabase/*|data/*|package.json|.env.example)
      needs_readme_update=true
      break
      ;;
    scripts/*)
      case "$file" in
        scripts/check-readme-staged.sh|scripts/install-git-hooks.sh)
          continue
          ;;
      esac
      needs_readme_update=true
      break
      ;;
  esac
done <<< "$STAGED"

if [[ "$needs_readme_update" != true ]]; then
  exit 0
fi

readme_has_staged_changes=false
if echo "$STAGED" | grep -qx 'README.md'; then
  if ! git diff --cached --quiet -- README.md; then
    readme_has_staged_changes=true
  fi
fi

if [[ "$readme_has_staged_changes" == true ]]; then
  exit 0
fi

cat >&2 <<'EOF'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 README reminder

 Staged changes touch app code, data, migrations, or tooling, but README.md
 was not updated in this commit.

 Please review README.md and stage updates if your change adds or alters:
   • User-facing features or flows
   • Routes, APIs, or environment variables
   • Migrations, seeds, or setup steps
   • Admin or facility behavior

 To continue without updating README.md:
   git commit --no-verify
   SKIP_README_HOOK=1 git commit ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF

exit 1
