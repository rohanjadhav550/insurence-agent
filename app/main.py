from app.rags.insurence_chat import insurence_chat_ollama, insurence_chat_gemini
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.connection import get_db, get_b2b_db
import uuid

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    thread: str

@app.get("/")
def read_root():
    return {"response":"Hello World"}

@app.post("/api/insurance-chat")
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    prompt = request.prompt
    thread = request.thread
    return StreamingResponse(
        insurence_chat_gemini(prompt, thread, db),
        media_type="text/event-stream"
    )

@app.post("/api/thread/new")
def create_thread(db: Session = Depends(get_db)):
    thread_id = str(uuid.uuid4())
    db.execute(
        text("INSERT INTO threads (thread_id) VALUES (:thread_id)"),
        {"thread_id": thread_id}
    )
    db.commit()
    return {"thread_id": thread_id}

# Validate thread exists (for continuing conversation)
@app.get("/api/thread/{thread_id}")
def get_thread(thread_id: str, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM threads WHERE thread_id = :thread_id"),
        {"thread_id": thread_id}
    ).fetchone()
    
    if not result:
        return {"exists": False}
    return {"exists": True, "thread_id": result.thread_id}

# Save a message
@app.post("/api/thread/{thread_id}/message")
def save_message(thread_id: str, role: str, content: str, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO messages (thread_id, role, content) VALUES (:thread_id, :role, :content)"),
        {"thread_id": thread_id, "role": role, "content": content}
    )
    db.commit()
    return {"status": "saved"}

# Fetch conversation history for a thread
@app.get("/api/thread/{thread_id}/messages")
def get_messages(thread_id: str, db: Session = Depends(get_db)):
    results = db.execute(
        text("SELECT role, content, created_at FROM messages WHERE thread_id = :thread_id ORDER BY created_at ASC"),
        {"thread_id": thread_id}
    ).fetchall()
    
    return [{"role": r.role, "content": r.content, "created_at": r.created_at} for r in results]

# Create a new conversation
@app.post("/api/conversation/new")
def create_conversation(db: Session = Depends(get_db)):
    thread_id = str(uuid.uuid4())
    
    db.execute(
        text("INSERT INTO threads (thread_id) VALUES (:thread_id)"),
        {"thread_id": thread_id}
    )
    db.execute(
        text("INSERT INTO conversations (thread_id, title) VALUES (:thread_id, :title)"),
        {"thread_id": thread_id, "title": "New Conversation"}
    )
    db.commit()
    return {"thread_id": thread_id}


# List all conversations (for sidebar/listing)
@app.get("/api/conversations")
def list_conversations(db: Session = Depends(get_db)):
    results = db.execute(
        text("""
            SELECT c.thread_id, c.title, c.created_at, c.updated_at,
                   (SELECT content FROM messages 
                    WHERE thread_id = c.thread_id 
                    ORDER BY created_at DESC LIMIT 1) AS last_message
            FROM conversations c
            ORDER BY c.updated_at DESC
        """)
    ).fetchall()

    return [
        {
            "thread_id": r.thread_id,
            "title": r.title,
            "last_message": r.last_message,
            "updated_at": r.updated_at
        } for r in results
    ]


# Auto-update title from first user message
@app.patch("/api/conversation/{thread_id}/title")
def update_title(thread_id: str, db: Session = Depends(get_db)):
    first_message = db.execute(
        text("""
            SELECT content FROM messages 
            WHERE thread_id = :thread_id AND role = 'user' 
            ORDER BY created_at ASC LIMIT 1
        """),
        {"thread_id": thread_id}
    ).fetchone()

    if first_message:
        # Truncate to 50 chars as title
        title = first_message.content[:50] + ("..." if len(first_message.content) > 50 else "")
        db.execute(
            text("UPDATE conversations SET title = :title WHERE thread_id = :thread_id"),
            {"title": title, "thread_id": thread_id}
        )
        db.commit()

    return {"status": "updated"}

@app.get('/api/b2b/health')
def b2b_db_health(db: Session = Depends(get_b2b_db)):
    result = db.execute(text("SELECT * FROM city LIMIT 1")).fetchall()
    if result is not None:
        return True
    else: 
        return "Connection failed"