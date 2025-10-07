#!/bin/bash
# Script para desarrollo local - carga el .env y luego inicia uvicorn

# Load .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Loaded .env file for local development"
else
    echo "⚠️  No .env file found"
fi

# Start uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
