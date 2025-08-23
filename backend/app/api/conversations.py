"""
Conversations API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from pydantic import BaseModel
import uuid
from datetime import datetime

from app.services.database import get_db
from app.services.gemma_service import GemmaService
from app.models.database import Conversation, Patient
from sqlalchemy import select

router = APIRouter()

class ConversationRequest(BaseModel):
    patient_id: int
    content: str
    session_id: Optional[str] = None
    interaction_type: str = "text"

class ConversationResponse(BaseModel):
    id: int
    content: str
    response: str
    mood_score: Optional[float]
    cognitive_score: Optional[float]
    timestamp: datetime

class MultimodalRequest(BaseModel):
    patient_id: int
    text_prompt: str
    session_id: Optional[str] = None

@router.post("/text", response_model=ConversationResponse)
async def create_text_conversation(
    request: ConversationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a text-based conversation"""
    
    # Verify patient exists
    patient_result = await db.execute(select(Patient).where(Patient.id == request.patient_id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Get AI response using Gemma service
    gemma_service = GemmaService()
    ai_response = await gemma_service.generate_text(
        prompt=request.content,
        system_prompt=f"المريض: {patient.name}, العمر: {patient.age}, المرحلة: {patient.diagnosis_stage}"
    )
    
    # Create conversation record
    conversation = Conversation(
        patient_id=request.patient_id,
        session_id=session_id,
        content=request.content,
        response=ai_response,
        interaction_type=request.interaction_type,
        mood_score=0.7,  # TODO: Implement mood analysis
        cognitive_score=0.8  # TODO: Implement cognitive scoring
    )
    
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        content=conversation.content,
        response=conversation.response,
        mood_score=conversation.mood_score,
        cognitive_score=conversation.cognitive_score,
        timestamp=conversation.timestamp
    )

@router.post("/multimodal")
async def create_multimodal_conversation(
    request: MultimodalRequest,
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Create a multimodal conversation with text, image, and/or audio"""
    
    # Verify patient exists
    patient_result = await db.execute(select(Patient).where(Patient.id == request.patient_id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    gemma_service = GemmaService()
    session_id = request.session_id or str(uuid.uuid4())
    
    # Process based on available modalities
    if image and audio:
        # Full multimodal processing
        image_data = await image.read()
        audio_data = await audio.read()
        
        # Analyze image first
        image_response = await gemma_service.analyze_image_with_text(
            image_data=image_data,
            text_prompt=request.text_prompt,
            patient_context={"name": patient.name, "age": patient.age}
        )
        
        # Process audio with image context
        audio_analysis = await gemma_service.process_audio_with_context(
            audio_data=audio_data,
            context=f"الصورة: {image_response}. النص: {request.text_prompt}",
            patient_info={"name": patient.name, "stage": patient.diagnosis_stage}
        )
        
        final_response = f"{image_response}\n\nتحليل الصوت: {audio_analysis['analysis']}"
        
    elif image:
        # Image + text processing
        image_data = await image.read()
        final_response = await gemma_service.analyze_image_with_text(
            image_data=image_data,
            text_prompt=request.text_prompt,
            patient_context={"name": patient.name, "age": patient.age}
        )
        
    elif audio:
        # Audio + text processing
        audio_data = await audio.read()
        audio_analysis = await gemma_service.process_audio_with_context(
            audio_data=audio_data,
            context=request.text_prompt,
            patient_info={"name": patient.name, "stage": patient.diagnosis_stage}
        )
        final_response = audio_analysis['analysis']
        
    else:
        # Text only
        final_response = await gemma_service.generate_text(
            prompt=request.text_prompt,
            system_prompt=f"المريض: {patient.name}, العمر: {patient.age}"
        )
    
    # Save conversation
    conversation = Conversation(
        patient_id=request.patient_id,
        session_id=session_id,
        content=request.text_prompt,
        response=final_response,
        interaction_type="multimodal",
        image_path=f"uploads/{image.filename}" if image else None,
        audio_path=f"uploads/{audio.filename}" if audio else None,
        mood_score=0.75,
        cognitive_score=0.8
    )
    
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    
    return {
        "id": conversation.id,
        "response": final_response,
        "session_id": session_id,
        "timestamp": conversation.timestamp
    }

@router.get("/patient/{patient_id}")
async def get_patient_conversations(
    patient_id: int,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get conversations for a specific patient"""
    
    result = await db.execute(
        select(Conversation)
        .where(Conversation.patient_id == patient_id)
        .order_by(Conversation.timestamp.desc())
        .limit(limit)
    )
    conversations = result.scalars().all()
    
    return [
        {
            "id": conv.id,
            "content": conv.content,
            "response": conv.response,
            "interaction_type": conv.interaction_type,
            "mood_score": conv.mood_score,
            "cognitive_score": conv.cognitive_score,
            "timestamp": conv.timestamp
        }
        for conv in conversations
    ]

@router.get("/session/{session_id}")
async def get_session_conversations(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all conversations in a session"""
    
    result = await db.execute(
        select(Conversation)
        .where(Conversation.session_id == session_id)
        .order_by(Conversation.timestamp.asc())
    )
    conversations = result.scalars().all()
    
    return [
        {
            "id": conv.id,
            "content": conv.content,
            "response": conv.response,
            "timestamp": conv.timestamp
        }
        for conv in conversations
    ]
