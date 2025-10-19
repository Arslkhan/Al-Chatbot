"""
Legal Chatbot Backend - FastAPI Application
"""
import os
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Legal Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "")

# Store conversation history (in production, use a database)
conversations = {}


class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str


SYSTEM_PROMPT = """You are a knowledgeable legal assistant chatbot. Your role is to:
1. Provide general information about legal concepts and procedures
2. Help users understand their legal rights and obligations
3. Suggest when professional legal counsel should be sought
4. Explain legal terminology in simple terms

IMPORTANT DISCLAIMERS:
- You are NOT a licensed attorney and cannot provide legal advice
- Your responses are for informational purposes only
- Users should consult with a qualified attorney for specific legal matters
- You cannot represent users in legal proceedings

Always be professional, accurate, and helpful while maintaining these boundaries.
When discussing legal matters, remind users to seek professional legal counsel for their specific situation.
"""


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Legal Chatbot</h1><p>Frontend not found. Please ensure static/index.html exists.</p>"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat requests from users
    """
    try:
        # Generate or use existing session ID
        session_id = request.session_id or f"session_{datetime.utcnow().timestamp()}"
        
        # Initialize conversation history if needed
        if session_id not in conversations:
            conversations[session_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        
        # Add user message to history
        conversations[session_id].append({
            "role": "user",
            "content": request.message
        })
        
        # Check if API key is configured
        if not openai.api_key:
            # Return a mock response if no API key
            mock_response = """Thank you for your question. 

**IMPORTANT DISCLAIMER**: This is a demonstration chatbot. For actual legal assistance:
- Consult with a licensed attorney in your jurisdiction
- Contact your local bar association for referrals
- Consider legal aid services if you qualify

To use the full AI-powered features of this chatbot, please configure your OpenAI API key in the .env file.

Is there anything specific about legal processes or terminology I can help explain in general terms?"""
            
            conversations[session_id].append({
                "role": "assistant",
                "content": mock_response
            })
            
            return ChatResponse(
                response=mock_response,
                session_id=session_id,
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversations[session_id],
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversations[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return ChatResponse(
            response=assistant_message,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/api/conversations/{session_id}")
async def get_conversation(session_id: str):
    """
    Retrieve conversation history for a session
    """
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Filter out system messages
    user_messages = [
        msg for msg in conversations[session_id] 
        if msg["role"] != "system"
    ]
    
    return {"session_id": session_id, "messages": user_messages}


@app.delete("/api/conversations/{session_id}")
async def clear_conversation(session_id: str):
    """
    Clear conversation history for a session
    """
    if session_id in conversations:
        # Keep only system prompt
        conversations[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        return {"message": "Conversation cleared", "session_id": session_id}
    
    raise HTTPException(status_code=404, detail="Session not found")


# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    pass  # Static directory doesn't exist yet


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

