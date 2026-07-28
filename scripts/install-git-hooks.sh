#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Skip on CI / Render — hooks are for local commits only.
if [[ "${CI:-}" == "true" || "${RENDER:-}" == "true" ]]; then
  echo "CI/Render environment; skipping hook install."
  exit 0
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not a git repository; skipping hook install." >&2
  exit 0
fi

chmod +x "$ROOT/.githooks/pre-commit" "$ROOT/scripts/check-readme-staged.sh"

git config core.hooksPath .githooks

echo "Git hooks installed (core.hooksPath=.githooks)"
