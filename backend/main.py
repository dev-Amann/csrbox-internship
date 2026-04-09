import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

from agent import app as langgraph_app
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="PathEdge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

supabase_available = bool(url and key)
if supabase_available:
    try:
        supabase: Client = create_client(url, key)
    except Exception as e:
        print(f"Failed to init Supabase: {e}")
        supabase_available = False
else:
    print("Supabase credentials not found. DB logging disabled.")
    supabase = None

# A single message in the history sent from the frontend
class MessageItem(BaseModel):
    role: str   # "user" or "ai"
    text: str

class ChatRequest(BaseModel):
    message: str
    # Full conversation history from frontend (for stateless serverless operation)
    message_history: Optional[List[MessageItem]] = []
    # Current profile state tracked by frontend
    session_state: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    state: Dict[str, Any]
    is_finished: bool

def parse_state_for_frontend(state: dict) -> dict:
    return {
        "student_name": state.get("student_name"),
        "target_role": state.get("target_role"),
        "core_skills": state.get("core_skills"),
        "location": state.get("location"),
        "interview_type": state.get("interview_type"),
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Reconstruct message history from frontend payload
        history_messages = []
        for msg in (request.message_history or []):
            if msg.role == "user":
                history_messages.append(HumanMessage(content=msg.text))
            elif msg.role == "ai":
                history_messages.append(AIMessage(content=msg.text))

        # Add the new user message
        history_messages.append(HumanMessage(content=request.message))

        # Build initial state from session_state sent by frontend
        initial_state = {
            "messages": history_messages,
            "student_name": request.session_state.get("student_name"),
            "target_role": request.session_state.get("target_role"),
            "core_skills": request.session_state.get("core_skills"),
            "location": request.session_state.get("location"),
            "interview_type": request.session_state.get("interview_type"),
            "is_finished": False,
            "feedback_summary": None,
        }

        # Invoke stateless LangGraph (no thread config needed)
        result = langgraph_app.invoke(initial_state)

        # Get last AI message
        last_message = result["messages"][-1].content
        is_finished = result.get("is_finished", False)

        # Log to Supabase if interview is finished
        if is_finished and supabase_available:
            try:
                supabase.table("interview_sessions").insert({
                    "student_name": result.get("student_name", "Unknown"),
                    "target_role": result.get("target_role", "Unknown"),
                    "interview_type": result.get("interview_type", "Unknown"),
                    "feedback_summary": result.get("feedback_summary", "Session Completed")
                }).execute()
            except Exception as e:
                print(f"Supabase logging error: {e}")

        return ChatResponse(
            response=last_message,
            state=parse_state_for_frontend(result),
            is_finished=is_finished
        )

    except Exception as e:
        print(f"Error handling /api/chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
