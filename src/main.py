from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent import chat_with_agent


app = FastAPI(
    title="MediAssist AI",
    description="AI-powered hospital assistant using RAG and AI tools",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: list[str] = []
    ticket_id: int | None = None
    ticket_status: str | None = None
    tools: list[str] = []


@app.get("/")
def root():
    return {
        "message": "MediAssist AI API is running"
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:

        result = chat_with_agent(request.message)

        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            ticket_id=result["ticket_id"],
            ticket_status=result["ticket_status"],
            tools=result["tools"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the request."
        )