# /opt/genesys-full/backend/tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from app import app, START_TIME, REQUEST_COUNT, blueprints, agents

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "timestamp" in body

def test_list_blueprints():
    resp = client.get("/blueprint")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(bp["id"] == "bp-123" for bp in data)

def test_create_agent_and_counts():
    initial_agents = len(agents)
    initial_requests = REQUEST_COUNT

    payload = {"name":"UTAgent","blueprint_id":"bp-123","config":{}}
    resp = client.post("/agents", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["message"] == "Agent created"
    assert body["agent"]["name"] == "UTAgent"

    st = client.get("/status")
    mt = client.get("/metrics")
    assert st.status_code == mt.status_code == 200

    stj = st.json(); mtj = mt.json()
    assert stj["agent_count"] == initial_agents + 1
    assert mtj["agents_created"] >= 1
    assert mtj["total_requests"] >= initial_requests + 3

@pytest.mark.parametrize("path,method", [
    ("/blueprint","get"), ("/health","get"),
    ("/status","get"),    ("/metrics","get"),
])
def test_endpoints_return_ok(path, method):
    resp = getattr(client, method)(path)
    assert resp.status_code == 200
