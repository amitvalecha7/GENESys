#!/bin/bash

echo "🧹 Cleaning up old frontend container..."
docker rm -f genesys-frontend-1 2>/dev/null

echo "📦 Writing fixed app.py with proper backend URL..."
cat <<EOF > /opt/genesys-full/frontend/app.py
import streamlit as st
import requests

st.set_page_config(page_title="GENESYS Console", layout="wide")
st.title("GENESYS Console Test")

try:
    r = requests.get("http://genesys-backend-1:3011/health", timeout=5)
    if r.status_code == 200:
        st.success("✅ Backend is healthy")
    else:
        st.error(f"❌ Backend returned: {r.status_code}")
except Exception as e:
    st.error(f"❌ Failed to connect to backend: {e}")
EOF

echo "🔧 Rebuilding frontend Docker image..."
cd /opt/genesys-full/frontend || exit 1
docker build -t genesys-frontend .

echo "🚀 Running frontend container on 'genesys-net'..."
docker run -d \
  --name genesys-frontend-1 \
  --network genesys-net \
  -p 3012:3012 \
  genesys-frontend

echo "✅ GENESYS Console frontend deployed at: http://localhost:3012"
echo "🔗 Or visit: https://console.dhii.ai (via NGINX)"
