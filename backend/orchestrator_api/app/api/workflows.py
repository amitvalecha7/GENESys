from fastapi import APIRouter
from typing import List, Dict
from app.services.agent_manager import DiscoveryAgent

router = APIRouter()

@router.post("/discover", response_model=List[Dict])
async def discover(nodes: List[Dict]):
    """
    Discover OS info and containers on provided nodes.
    """
    return DiscoveryAgent.discover_nodes(nodes)

from pydantic import BaseModel

class DocRequest(BaseModel):
    title: str
    details: dict

class DocResponse(BaseModel):
    document_url: str

@router.post("/generate-manual", response_model=DocResponse)
async def generate_manual(payload: DocRequest):
    """
    Stub: In future this will invoke DocAgent to build and store an operational manual.
    """
    # For now, return a placeholder link
    return DocResponse(document_url="https://docs.example.com/manuals/operational_manual.md")
