#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -f "$ROOT/python/.venv/bin/uvicorn" ]; then
  echo "Run ./scripts/setup.sh first."
  exit 1
fi

cleanup() {
  kill "$API_PID" "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Starting Pulse API on http://localhost:8000 ..."
(
  cd "$ROOT/python"
  export PYTHONPATH=src
  exec .venv/bin/uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
) &
API_PID=$!

echo "Starting Pulse UI on http://localhost:5173 ..."
(
  cd "$ROOT/javascript"
  exec npm run dev -- --host 127.0.0.1
) &
FRONTEND_PID=$!

echo ""
echo "Pulse is running (Ctrl+C to stop both):"
echo "  API:  http://localhost:8000/health"
echo "  UI:   http://localhost:5173"
echo ""

wait
