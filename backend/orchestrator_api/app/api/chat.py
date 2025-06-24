from fastapi import APIRouter
from app.models.chat_models import ChatRequest, ChatResponse

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/message", response_model=ChatResponse)
async def chat_message(req: ChatRequest):
    # Placeholder logic until matrix_router is wired
    return ChatResponse(reply=f"Echo: {req.message}")
