import os
from typing import TypedDict, Annotated, List, Optional, Literal
import operator
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# Make sure you have GROQ_API_KEY set in .env
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# Define State
class InterviewState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    student_name: Optional[str]
    target_role: Optional[str]
    core_skills: Optional[str]
    location: Optional[str]
    interview_type: Optional[str]
    is_finished: bool
    feedback_summary: Optional[str]

# Define structured output for router to extract state
class RouterOutput(BaseModel):
    is_info_complete: bool = Field(description="True if we have enough info to start an interview.")
    student_name: Optional[str] = Field(description="Extracted student name")
    target_role: Optional[str] = Field(description="Extracted target role")
    core_skills: Optional[str] = Field(description="Extracted core skills")
    location: Optional[str] = Field(description="Extracted geographical location (city, state, country, etc.)")
    interview_type: Optional[str] = Field(description="Extracted interview type (Technical, HR, Resume Review, Job Prediction)")
    response_message: Optional[str] = Field(description="Message to send to user if info is incomplete")

def router_node(state: InterviewState):
    """
    Determines if we should ask for more info or route to the specific interview mode.
    """
    system_prompt = f"""You are PathEdge, an AI career portal.
    Current gathered info:
    Name: {state.get("student_name")}
    Role: {state.get("target_role")}
    Skills: {state.get("core_skills")}
    Location: {state.get("location")}
    Type: {state.get("interview_type")}

    If info is incomplete, ask the user to provide the missing pieces (especially Location for Job Prediction) nicely in `response_message`.
    If complete, set `is_info_complete` to true. If user wants to stop, you can handle it.
    """
    
    # We use structured output to map to state variables
    structured_llm = llm.with_structured_output(RouterOutput)
    
    # Construct conversation
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response: RouterOutput = structured_llm.invoke(messages)
    
    # Update state
    updates = {}
    if response.student_name: updates["student_name"] = response.student_name
    if response.target_role: updates["target_role"] = response.target_role
    if response.core_skills: updates["core_skills"] = response.core_skills
    if response.location: updates["location"] = response.location
    if response.interview_type: updates["interview_type"] = response.interview_type
    
    if not response.is_info_complete:
        # Ask user for info
        updates["messages"] = [AIMessage(content=response.response_message or "Please tell me more about yourself.")]
    return updates

def route_after_init(state: InterviewState):
    """Conditional Edge function"""
    # If info not complete, go back to user (END) to wait for input
    if not state.get("student_name") or not state.get("target_role") or not state.get("interview_type"):
        return END
        
    type_lower = str(state.get("interview_type")).lower()
    if "predict" in type_lower or "job" in type_lower:
        # Require location for prediction
        if not state.get("location"):
             return END
        return "predict_node"
    elif "tech" in type_lower:
        return "technical_node"
    elif "hr" in type_lower or "behavior" in type_lower:
        return "hr_node"
    else:
        return "resume_node"

def generate_interview_response(state: InterviewState, prompt_instructions: str):
    messages = [SystemMessage(content=prompt_instructions)] + state["messages"]
    response = llm.invoke(messages)
    
    # Very basic end condition checking
    is_end = "stop" in str(state["messages"][-1].content).lower() if state["messages"] else False
    if is_end:
        feedback_summary_instruction = "Summarize the student's performance in this session."
        summary_res = llm.invoke([SystemMessage(content=feedback_summary_instruction)] + state["messages"])
        return {"messages": [response], "is_finished": True, "feedback_summary": summary_res.content}
        
    return {"messages": [response]}

def technical_node(state: InterviewState):
    instructions = f"""You are conducting a Technical Mock Interview for a {state.get("target_role")}.
    The student's core skills are: {state.get("core_skills")}.
    First, provide immediate, constructive feedback to their previous answer. Then, ask ONE technical question.
    Wait for their response."""
    return generate_interview_response(state, instructions)

def hr_node(state: InterviewState):
    instructions = f"""You are an HR Manager conducting a Behavioral Mock Interview for a {state.get("target_role")} role.
    First, provide immediate, constructive feedback to their previous answer. Then, ask ONE behavioral/HR question (e.g., conflict resolution, teamwork).
    Wait for their response."""
    return generate_interview_response(state, instructions)

def resume_node(state: InterviewState):
    instructions = f"""You are a Career Counselor reviewing a resume for a {state.get("target_role")} role.
    Student skills: {state.get("core_skills")}.
    First, provide constructive feedback on their previous answer. Then, ask ONE question about their projects or experience to help them improve their resume phrasing.
    Wait for their response."""
    return generate_interview_response(state, instructions)

def predict_node(state: InterviewState):
    instructions = f"""You are a Job Market Analyst.
    Student skills: {state.get("core_skills")}. Location: {state.get("location")}. Target Role: {state.get("target_role")}.
    Analyze their skills against their geographical market. Generate a highly detailed report containing:
    1. Realistic job titles to target.
    2. Local or remote companies they should apply to in {state.get("location")}.
    3. Missing skills they need to learn to be highly competitive there.
    Ask if they want to review a specific role further."""
    return generate_interview_response(state, instructions)

# Build Graph
workflow = StateGraph(InterviewState)

workflow.add_node("router", router_node)
workflow.add_node("technical_node", technical_node)
workflow.add_node("hr_node", hr_node)
workflow.add_node("resume_node", resume_node)
workflow.add_node("predict_node", predict_node)

workflow.add_edge(START, "router")
workflow.add_conditional_edges("router", route_after_init, {
    END: END,
    "technical_node": "technical_node",
    "hr_node": "hr_node",
    "resume_node": "resume_node",
    "predict_node": "predict_node"
})

workflow.add_edge("technical_node", END)
workflow.add_edge("hr_node", END)
workflow.add_edge("resume_node", END)
workflow.add_edge("predict_node", END)

# Stateless compile — session state is managed on the client (frontend)
# This makes the backend fully serverless-compatible (Vercel, AWS Lambda, etc.)
app = workflow.compile()
