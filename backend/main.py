import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from langchain_core.messages import HumanMessage
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

class ChatRequest(BaseModel):
    session_id: str
    message: str

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
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Invoke LangGraph
        result = langgraph_app.invoke(
            {"messages": [HumanMessage(content=request.message)]}, 
            config=config
        )
        
        # Get last message
        last_message = result["messages"][-1].content
        is_finished = result.get("is_finished", False)
        
        # Log to supabase if finished
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
