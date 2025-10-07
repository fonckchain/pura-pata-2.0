#!/bin/bash
# Railway startup script

echo "========================================="
echo "Starting Pura Pata API"
echo "========================================="

# Run healthcheck
python healthcheck.py || exit 1

# Set default port if not provided
PORT=${PORT:-8000}

echo ""
echo "Starting uvicorn on port $PORT..."
echo ""

# Start uvicorn
uvicorn app.main:app --host 0.0.0.0 --port $PORT
