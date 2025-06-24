from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.workflows import router as wf_router

app = FastAPI(title="Genesys Orchestrator API")
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(wf_router, prefix="/workflows", tags=["Workflows"])
