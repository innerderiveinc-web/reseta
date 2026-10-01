#!/bin/zsh
set -e

cd "$(dirname "$0")"

APP_DIR="$PWD"
PORT="${1:-${PORT:-8123}}"
URL="http://127.0.0.1:${PORT}"
LOG_FILE="/tmp/reseta_enterprise_backend.log"
PYTHON_BIN="$APP_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Python virtual environment not found at $PYTHON_BIN"
  echo "Setting up virtual environment..."
  /usr/bin/python3 -m venv "$APP_DIR/.venv"
fi

export PYTHONPATH="$APP_DIR:$PYTHONPATH"

# Run tests before launch
echo "Running RESETA™ Enterprise verification tests..."
"$PYTHON_BIN" -m pytest tests/ -q

echo "Seeding initial enterprise dataset..."
"$PYTHON_BIN" backend/seeds.py

echo "Launching RESETA™ Enterprise at ${URL}"
"$PYTHON_BIN" -m uvicorn backend.main:app --host 127.0.0.1 --port "$PORT" >"$LOG_FILE" 2>&1 &
SERVER_PID=$!

sleep 1.5

if command -v open >/dev/null 2>&1; then
  open "$URL"
fi

echo "=========================================================="
echo "  RESETA™ ENTERPRISE SERVER IS RUNNING"
echo "  URL:      ${URL}"
echo "  API Docs: ${URL}/api/docs"
echo "  Logs:     ${LOG_FILE}"
echo "=========================================================="
echo "Press Control+C in this terminal window to stop the server."

trap 'kill $SERVER_PID 2>/dev/null' EXIT INT TERM
wait $SERVER_PID
