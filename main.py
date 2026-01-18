from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict, Any, List
import os
import requests
import uuid

app = FastAPI()

# In-memory sessions
sessions: Dict[str, Dict[str, Any]] = {}

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    mode: str
    reply: str
    meta: Dict[str, Any] | None = None

def get_session(session_id: str = Header(None, alias="x-session-id")):
    if not session_id:
        session_id = str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = {"mode": "assistant", "history": []}
    return session_id, sessions[session_id]

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
NORMAL_KEY = os.getenv("NORMAL_API_KEY")
MATRIX_KEY = os.getenv("MATRIX_API_KEY")

def verify_key(key: str = Header(..., alias="x-api-key")):
    if key == NORMAL_KEY:
        return "assistant"
    if key == MATRIX_KEY:
        return "matrix"
    raise HTTPException(401, "Invalid API key")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, allowed_mode: str = Depends(verify_key), session_id: str = Depends(get_session)[0], session: Dict = Depends(get_session)[1]):
    history = session["history"]
    history.append({"role": "user", "content": request.message})
    
    if "matrix" in request.message.lower():
        session["mode"] = "matrix"
        reply = matrix_engine(request.message, history)
    else:
        if session["mode"] == "matrix":
            session["mode"] = "assistant"
        reply = llm_chat(history)
    
    history.append({"role": "assistant", "content": reply})
    if len(history) > 10:
        history[:] = history[-10:]
    
    return ChatResponse(mode=session["mode"], reply=reply)

def llm_chat(history: List[Dict]):
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": history,
        "stream": False
    }
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    return "LLM error, using fallback: Helpful response here."

def matrix_engine(query: str, history: List):
    # Planner
    goal = "Achieve optimal outcome"
    constraints = ["time", "risk"]
    
    # Simulator: Generate 3 paths
    paths = [
        {"name": "Aggressive", "success_prob": 0.7, "risk": "high", "impact": "major"},
        {"name": "Balanced", "success_prob": 0.85, "risk": "medium", "impact": "solid"},
        {"name": "Conservative", "success_prob": 0.95, "risk": "low", "impact": "minor"}
    ]
    
    # Evaluator: Pick best
    impact_scores = {"major": 3, "solid": 2, "minor": 1}
    scores = {p["name"]: p["success_prob"] * impact_scores[p["impact"]] for p in paths}
    chosen = max(scores, key=scores.get)
    confidence = scores[chosen] * 100
    
    reason = f"Selected {chosen} balancing prob {paths[1]['success_prob']} and impact."
    reply = f"Chosen Path: {chosen}\n\nWhy:\n{reason}\n\nConfidence: {confidence:.0f}%"
    return reply

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
