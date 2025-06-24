import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(page_title="GENESYS Console", layout="wide")
st.title("GENESYS Console")

# ─── Load & Display Blueprints ────────────────────────────────────────────────
@st.cache_data
def load_blueprints():
    resp = requests.get("http://backend:3011/blueprint")
    resp.raise_for_status()
    return resp.json()

with st.spinner("Fetching blueprints…"):
    blueprints = load_blueprints()

bp_ids = [bp["id"] for bp in blueprints]
selected_bp = st.selectbox("Filter by Blueprint ID", ["All"] + bp_ids)
if selected_bp != "All":
    blueprints = [bp for bp in blueprints if bp["id"] == selected_bp]

st.subheader("Available Blueprints")
st.dataframe(pd.DataFrame(blueprints))

# ─── Agent Creation Form ───────────────────────────────────────────────────────
st.subheader("Create a New Agent")
with st.form("agent_form"):
    name = st.text_input("Agent Name")
    bp_id = st.selectbox("Blueprint", bp_ids)
    cfg_text = st.text_area("Config (JSON)", "{}")
    submitted = st.form_submit_button("Create Agent")

    if submitted:
        with st.spinner("Creating agent…"):
            try:
                payload = {
                    "name": name,
                    "blueprint_id": bp_id,
                    "config": json.loads(cfg_text)
                }
                res = requests.post("http://backend:3011/agents", json=payload)
                res.raise_for_status()
                st.success("✅ Agent created!")
                st.json(res.json())
            except Exception as e:
                st.error(f"Failed to create agent:\n{e}")

# ─── Service Status & Metrics ─────────────────────────────────────────────────
st.subheader("Service Status & Metrics")

with st.spinner("Loading status…"):
    resp = requests.get("http://backend:3011/status")
    resp.raise_for_status()
    status_info = resp.json()

st.write(f"**Uptime:** {status_info['uptime']:.1f} seconds")
st.write(f"**Blueprints:** {status_info['blueprint_count']}")
st.write(f"**Agents:** {status_info['agent_count']}")

with st.spinner("Loading metrics…"):
    resp2 = requests.get("http://backend:3011/metrics")
    resp2.raise_for_status()
    met = resp2.json()

st.write(f"**Total Requests:** {met['total_requests']}")
st.write(f"**Agents Created:** {met['agents_created']}")
