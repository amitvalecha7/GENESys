#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "🔨 Building backend image..."
docker build -t genesys-full-backend:latest .

echo "🛑 Stopping old container..."
docker rm -f genesys-backend || true

echo "🚀 Starting backend on genesys-net..."
docker run -d \
  --name genesys-backend \
  --network genesys-net \
  -p 3011:3011 \
  genesys-full-backend:latest

echo "✅ Backend is up at http://backend:3011 (inside network) and http://localhost:3011 (host)."
