from fastapi import FastAPI
from app.chatbot import handle_message
from pydantic import BaseModel

app = FastAPI(
    title="Property AI Chatbot",
    description="Conversational property search API",
    version="1.0"
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
def chat(data: ChatRequest):

    session_id = data.session_id
    message = data.message

    reply = handle_message(session_id, message)

    return {"reply": reply}