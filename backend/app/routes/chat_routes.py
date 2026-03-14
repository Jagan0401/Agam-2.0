from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.dependencies import get_db
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])

class ChatRequest(BaseModel):
    message: str
    language: str = "english"

@router.post("/")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Endpoint for the Agam Intelligence chatbot.
    """
    reply = ChatService.process_message(db, req.message, req.language)
    return {"reply": reply}
