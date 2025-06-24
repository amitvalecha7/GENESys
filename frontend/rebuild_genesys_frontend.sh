#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "🔨 Building frontend image..."
docker build -t genesys-full-frontend:latest .

echo "🛑 Stopping old container..."
docker rm -f genesys-frontend || true

echo "🚀 Starting frontend on genesys-net..."
docker run -d \
  --name genesys-frontend \
  --network genesys-net \
  -p 3012:3012 \
  genesys-full-frontend:latest

echo "✅ Frontend is up at http://frontend:3012 (inside network) and http://localhost:3012 (host)."
