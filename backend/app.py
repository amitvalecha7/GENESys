from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict
import time

app = FastAPI(title="GENESYS Backend")

# ─── Models ────────────────────────────────────────────────────────────────────
class Blueprint(BaseModel):
    id: str
    name: str
    created_at: datetime

class AgentCreate(BaseModel):
    name: str
    blueprint_id: str
    config: Dict

# ─── In-Memory Stores ───────────────────────────────────────────────────────────
blueprints: List[Blueprint] = [
    Blueprint(id="bp-123", name="Default Blueprint", created_at=datetime.utcnow())
]
agents: List[Dict] = []

# ─── Runtime Metrics ───────────────────────────────────────────────────────────
START_TIME = time.time()
REQUEST_COUNT = 0

@app.middleware("http")
async def count_requests(request: Request, call_next):
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    return await call_next(request)

# ─── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/blueprint", response_model=List[Blueprint])
def list_blueprints():
    """
    Return all available blueprints.
    """
    return blueprints

@app.post("/agents", status_code=201)
def create_agent(payload: AgentCreate):
    """
    Create a new agent based on a blueprint.
    """
    if not any(bp.id == payload.blueprint_id for bp in blueprints):
        raise HTTPException(status_code=404, detail="Blueprint not found")

    new_agent = {
        "name": payload.name,
        "blueprint_id": payload.blueprint_id,
        "config": payload.config,
        "created_at": datetime.utcnow()
    }
    agents.append(new_agent)
    return {"message": "Agent created", "agent": new_agent}

@app.get("/health")
def health_check():
    """
    Liveness probe.
    """
    return {"status": "ok", "timestamp": datetime.utcnow()}

@app.get("/status")
def status():
    """
    Service status: uptime and counts.
    """
    return {
        "uptime": time.time() - START_TIME,
        "blueprint_count": len(blueprints),
        "agent_count": len(agents)
    }

@app.get("/metrics")
def metrics():
    """
    Usage metrics: total HTTP requests and agents created.
    """
    return {
        "total_requests": REQUEST_COUNT,
        "agents_created": len(agents)
    }
