#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Setting up Pulse (Python + Node, no Docker required)..."

cd "$ROOT/python"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -r requirements.txt

cd "$ROOT/javascript"
npm install

echo ""
echo "Setup complete. Start the app with:"
echo "  make dev"
echo "Or in two terminals:"
echo "  make dev-api"
echo "  make dev-frontend"
