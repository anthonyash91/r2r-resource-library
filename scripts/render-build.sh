#!/usr/bin/env bash
# Render / production build: Next.js standalone + static assets.
set -euo pipefail

npm install --include=dev
npm run build

test -f .next/standalone/server.js

mkdir -p .next/standalone/.next
rm -rf .next/standalone/public .next/standalone/.next/static
cp -R public .next/standalone/public
cp -R .next/static .next/standalone/.next/static

echo "Standalone build ready:"
ls -la .next/standalone/server.js .next/standalone/public .next/standalone/.next/static | head
