#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "🔨 Building backend image (with tests)…"
docker build -t genesys-full-backend:latest .

echo "🛑 Removing old container (if any)…"
docker rm -f genesys-backend || true

echo "🚀 Starting backend container on genesys-net…"
docker run -d \
  --name genesys-backend \
  --network genesys-net \
  -p 3011:3011 \
  genesys-full-backend:latest

# Wait a sec for the container to come up
sleep 2

echo "🧪 Running pytest inside container with PYTHONPATH=/app…"
docker exec -e PYTHONPATH=/app -it genesys-backend pytest -q

echo "✅ All tests passed! Cleaning up…"
docker rm -f genesys-backend
