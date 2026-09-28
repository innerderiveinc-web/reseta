#!/usr/bin/env bash
set -e

PORT="${1:-8000}"
export PYTHONPATH=".:$PYTHONPATH"

echo "Starting RESETA™ Enterprise on port $PORT..."
./.venv/bin/python backend/seeds.py
exec ./.venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port "$PORT"
