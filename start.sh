#!/usr/bin/env bash
set -e

PORT="${1:-${PORT:-8123}}"
export PYTHONPATH=".:$PYTHONPATH"

echo "Starting RESETA™ Enterprise on port $PORT..."
./.venv/bin/python backend/seeds.py
exec ./.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port "$PORT"

