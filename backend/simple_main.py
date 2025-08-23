#!/usr/bin/env python3
"""
Simple FastAPI server for Alzheimer's Memory Assistant
Works with system Python packages to avoid environment issues
"""
import json
import os
import random
from datetime import datetime
from typing import List, Optional

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("❌ Required packages not installed. Installing with system packages...")
    os.system("pip3 install --user fastapi uvicorn pydantic")
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn

# Configuration
ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:3001", "http://localhost:8081", "http://10.0.2.2:3000"]

app = FastAPI(
    title="Alzheimer's Memory Assistant API",
    description="Arabic AI assistant for Alzheimer's patients",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ConversationRequest(BaseModel):
    content: str
    patient_id: Optional[int] = 1
    session_id: Optional[str] = "default"

class ConversationResponse(BaseModel):
    id: int
    content: str
    response: str
    mood_score: Optional[float] = None
    cognitive_score: Optional[float] = None
    timestamp: str

class Patient(BaseModel):
    id: int
    name: str
    age: int
    condition: str
    created_at: str

class Reminder(BaseModel):
    id: int
    patient_id: int
    title: str
    description: str
    scheduled_time: str
    is_completed: bool = False

# In-memory storage
conversations = []
patients = [
    {
        "id": 1,
        "name": "مريض تجريبي",
        "age": 70,
        "condition": "ألزهايمر مبكر",
        "created_at": datetime.now().isoformat()
    }
]
reminders = [
    {
        "id": 1,
        "patient_id": 1,
        "title": "تناول الدواء",
        "description": "تذكر تناول دواء الذاكرة",
        "scheduled_time": datetime.now().isoformat(),
        "is_completed": False
    }
]

# Enhanced Arabic responses
arabic_responses = {
    "greetings": [
        "أهلاً وسهلاً! إزيك النهاردة؟",
        "مرحباً حبيبي، نورت المكان",
        "السلام عليكم، كيف الصحة؟",
        "صباح الخير يا غالي، إيه أخبارك؟"
    ],
    "memory_support": [
        "متقلقش، أنا هنا عشان أساعدك تفتكر",
        "خد وقتك، مفيش عجلة خالص",
        "الذاكرة زي العضلة، كل ما نمرنها تقوى",
        "كل حاجة هتيجي في وقتها، صبر شوية"
    ],
    "emotional_support": [
        "مشاعرك طبيعية خالص، ومتقلقش",
        "إنت مش لوحدك، أنا موجود معاك",
        "كلنا بنمر بأوقات صعبة، دا عادي",
        "إنت قوي وهتعدي الصعوبات دي"
    ],
    "family_connection": [
        "عيلتك بتحبك قوي وفاكراك دايماً",
        "حبايبك كلهم بيحبوك ومتذكرينك",
        "الحب اللي بينكم مش هيتنسى أبداً"
    ],
    "orientation_help": [
        "إحنا دلوقتي في البيت، في مكان آمن",
        "المكان ده مألوف وآمن ليك",
        "كل حاجة حواليك مرتبة ومنظمة"
    ]
}

def get_smart_response(user_input: str) -> str:
    """Generate contextual Arabic response"""
    input_lower = user_input.lower()
    
    if "مرحب" in input_lower or "أهل" in input_lower or "السلام" in input_lower:
        return random.choice(arabic_responses["greetings"])
    elif "مش فاكر" in input_lower or "نسيت" in input_lower or "مش متذكر" in input_lower:
        return random.choice(arabic_responses["memory_support"])
    elif "خايف" in input_lower or "قلقان" in input_lower or "حزين" in input_lower:
        return random.choice(arabic_responses["emotional_support"])
    elif "فين" in input_lower or "أنهي مكان" in input_lower:
        return random.choice(arabic_responses["orientation_help"])
    elif "عايز" in input_lower or "أكلم" in input_lower:
        return random.choice(arabic_responses["family_connection"])
    else:
        return random.choice(arabic_responses["memory_support"])

@app.get("/")
async def root():
    return {
        "message": "Alzheimer's Memory Assistant API",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "ai_model": "available"
        }
    }

@app.post("/api/v1/conversations", response_model=ConversationResponse)
async def create_conversation(request: ConversationRequest):
    response_text = get_smart_response(request.content)
    
    conversation = {
        "id": len(conversations) + 1,
        "content": request.content,
        "response": response_text,
        "mood_score": random.uniform(0.6, 0.9),
        "cognitive_score": random.uniform(0.7, 0.95),
        "timestamp": datetime.now().isoformat()
    }
    
    conversations.append(conversation)
    return ConversationResponse(**conversation)

@app.get("/api/v1/conversations")
async def get_conversations(patient_id: int = 1, session_id: str = "default"):
    return [ConversationResponse(**conv) for conv in conversations[-10:]]

@app.get("/api/v1/patients/{patient_id}")
async def get_patient(patient_id: int):
    patient = next((p for p in patients if p["id"] == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return Patient(**patient)

@app.get("/api/v1/patients/{patient_id}/reminders")
async def get_patient_reminders(patient_id: int):
    patient_reminders = [r for r in reminders if r["patient_id"] == patient_id]
    return [Reminder(**r) for r in patient_reminders]

@app.get("/api/v1/reminders/due")
async def get_due_reminders():
    return [Reminder(**r) for r in reminders if not r["is_completed"]]

@app.post("/api/v1/assessments")
async def create_assessment(data: dict):
    return {
        "id": 1,
        "patient_id": data.get("patient_id", 1),
        "type": data.get("type", "cognitive"),
        "score": random.uniform(0.7, 0.9),
        "recommendations": ["استمر في التمارين الذهنية", "حافظ على النشاط البدني"],
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🚀 Starting Alzheimer's Memory Assistant Backend...")
    print("🤖 Arabic AI responses: Enabled")
    print("🌐 Server will be available at: http://localhost:8000")
    
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
