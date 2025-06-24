#!/usr/bin/env bash
set -euo pipefail

# Adjust if your container has a different name
CONTAINER="n8n"  

# Paths to your JSON definitions
WORKFLOWS=(
  "/opt/genesys-full/n8n_list_blueprints.json"
  "/opt/genesys-full/n8n_create_agent.json"
)

echo "🔄 Importing n8n workflows into container '$CONTAINER'…"

for WF in "${WORKFLOWS[@]}"; do
  BASENAME=$(basename "$WF")
  echo "  • Copying $BASENAME → /data/$BASENAME"
  docker cp "$WF" "$CONTAINER:/data/$BASENAME"

  echo "  • Importing $BASENAME via CLI"
  docker exec -i "$CONTAINER" n8n import:workflow --input="/data/$BASENAME"
done

echo "✅ All workflows imported!"
