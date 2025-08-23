"""
Reminders API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.services.database import get_db
from app.models.database import Reminder, Patient
from sqlalchemy import select, and_

router = APIRouter()

class ReminderCreate(BaseModel):
    patient_id: int
    title: str
    description: Optional[str] = None
    reminder_type: str  # medication, appointment, activity, social
    scheduled_time: datetime
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly
    priority: str = "medium"  # low, medium, high, urgent

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None

class ReminderResponse(BaseModel):
    id: int
    patient_id: int
    title: str
    description: Optional[str]
    reminder_type: str
    scheduled_time: datetime
    is_recurring: bool
    recurrence_pattern: Optional[str]
    is_completed: bool
    priority: str
    created_at: datetime

@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    reminder: ReminderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new reminder"""
    
    # Verify patient exists
    patient_result = await db.execute(select(Patient).where(Patient.id == reminder.patient_id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db_reminder = Reminder(
        patient_id=reminder.patient_id,
        title=reminder.title,
        description=reminder.description,
        reminder_type=reminder.reminder_type,
        scheduled_time=reminder.scheduled_time,
        is_recurring=reminder.is_recurring,
        recurrence_pattern=reminder.recurrence_pattern,
        priority=reminder.priority
    )
    
    db.add(db_reminder)
    await db.commit()
    await db.refresh(db_reminder)
    
    return ReminderResponse(
        id=db_reminder.id,
        patient_id=db_reminder.patient_id,
        title=db_reminder.title,
        description=db_reminder.description,
        reminder_type=db_reminder.reminder_type,
        scheduled_time=db_reminder.scheduled_time,
        is_recurring=db_reminder.is_recurring,
        recurrence_pattern=db_reminder.recurrence_pattern,
        is_completed=db_reminder.is_completed,
        priority=db_reminder.priority,
        created_at=db_reminder.created_at
    )

@router.get("/patient/{patient_id}")
async def get_patient_reminders(
    patient_id: int,
    upcoming_only: bool = False,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get reminders for a specific patient"""
    
    query = select(Reminder).where(Reminder.patient_id == patient_id)
    
    if upcoming_only:
        query = query.where(
            and_(
                Reminder.scheduled_time >= datetime.now(),
                Reminder.is_completed == False
            )
        )
    
    query = query.order_by(Reminder.scheduled_time.asc()).limit(limit)
    
    result = await db.execute(query)
    reminders = result.scalars().all()
    
    return [
        {
            "id": reminder.id,
            "title": reminder.title,
            "description": reminder.description,
            "reminder_type": reminder.reminder_type,
            "scheduled_time": reminder.scheduled_time,
            "is_recurring": reminder.is_recurring,
            "is_completed": reminder.is_completed,
            "priority": reminder.priority
        }
        for reminder in reminders
    ]

@router.get("/due")
async def get_due_reminders(
    patient_id: Optional[int] = None,
    hours_ahead: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get reminders that are due within specified hours"""
    
    now = datetime.now()
    due_time = now + timedelta(hours=hours_ahead)
    
    query = select(Reminder).where(
        and_(
            Reminder.scheduled_time >= now,
            Reminder.scheduled_time <= due_time,
            Reminder.is_completed == False
        )
    )
    
    if patient_id:
        query = query.where(Reminder.patient_id == patient_id)
    
    query = query.order_by(Reminder.scheduled_time.asc())
    
    result = await db.execute(query)
    reminders = result.scalars().all()
    
    return [
        {
            "id": reminder.id,
            "patient_id": reminder.patient_id,
            "title": reminder.title,
            "description": reminder.description,
            "reminder_type": reminder.reminder_type,
            "scheduled_time": reminder.scheduled_time,
            "priority": reminder.priority,
            "minutes_until_due": int((reminder.scheduled_time - now).total_seconds() / 60)
        }
        for reminder in reminders
    ]

@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: int,
    reminder_update: ReminderUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a reminder"""
    
    result = await db.execute(select(Reminder).where(Reminder.id == reminder_id))
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Update fields if provided
    update_data = reminder_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reminder, field, value)
    
    # Set completion time if marked as completed
    if reminder_update.is_completed and not reminder.completion_time:
        reminder.completion_time = datetime.now()
    
    await db.commit()
    await db.refresh(reminder)
    
    return ReminderResponse(
        id=reminder.id,
        patient_id=reminder.patient_id,
        title=reminder.title,
        description=reminder.description,
        reminder_type=reminder.reminder_type,
        scheduled_time=reminder.scheduled_time,
        is_recurring=reminder.is_recurring,
        recurrence_pattern=reminder.recurrence_pattern,
        is_completed=reminder.is_completed,
        priority=reminder.priority,
        created_at=reminder.created_at
    )

@router.post("/{reminder_id}/complete")
async def complete_reminder(
    reminder_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Mark a reminder as completed"""
    
    result = await db.execute(select(Reminder).where(Reminder.id == reminder_id))
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    reminder.is_completed = True
    reminder.completion_time = datetime.now()
    
    # Create next occurrence if recurring
    if reminder.is_recurring and reminder.recurrence_pattern:
        next_time = _calculate_next_occurrence(
            reminder.scheduled_time, 
            reminder.recurrence_pattern
        )
        
        if next_time:
            next_reminder = Reminder(
                patient_id=reminder.patient_id,
                title=reminder.title,
                description=reminder.description,
                reminder_type=reminder.reminder_type,
                scheduled_time=next_time,
                is_recurring=reminder.is_recurring,
                recurrence_pattern=reminder.recurrence_pattern,
                priority=reminder.priority
            )
            db.add(next_reminder)
    
    await db.commit()
    
    return {"message": "Reminder completed successfully"}

@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a reminder"""
    
    result = await db.execute(select(Reminder).where(Reminder.id == reminder_id))
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    await db.delete(reminder)
    await db.commit()
    
    return {"message": "Reminder deleted successfully"}

def _calculate_next_occurrence(current_time: datetime, pattern: str) -> Optional[datetime]:
    """Calculate next occurrence for recurring reminders"""
    
    if pattern == "daily":
        return current_time + timedelta(days=1)
    elif pattern == "weekly":
        return current_time + timedelta(weeks=1)
    elif pattern == "monthly":
        # Simple monthly calculation (same day next month)
        if current_time.month == 12:
            return current_time.replace(year=current_time.year + 1, month=1)
        else:
            return current_time.replace(month=current_time.month + 1)
    
    return None
