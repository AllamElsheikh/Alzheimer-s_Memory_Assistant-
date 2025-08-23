"""
Patients API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.services.database import get_db
from app.models.database import Patient
from sqlalchemy import select

router = APIRouter()

class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    diagnosis_stage: Optional[str] = "early"  # early, moderate, severe
    language_preference: str = "ar"
    cultural_background: Optional[str] = "egyptian"
    emergency_contacts: Optional[dict] = None
    medication_schedule: Optional[dict] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    diagnosis_stage: Optional[str] = None
    cultural_background: Optional[str] = None
    emergency_contacts: Optional[dict] = None
    medication_schedule: Optional[dict] = None

class PatientResponse(BaseModel):
    id: int
    name: str
    age: Optional[int]
    diagnosis_stage: Optional[str]
    language_preference: str
    cultural_background: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

@router.post("/", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new patient"""
    
    db_patient = Patient(
        name=patient.name,
        age=patient.age,
        diagnosis_stage=patient.diagnosis_stage,
        language_preference=patient.language_preference,
        cultural_background=patient.cultural_background,
        emergency_contacts=patient.emergency_contacts,
        medication_schedule=patient.medication_schedule
    )
    
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    
    return PatientResponse(
        id=db_patient.id,
        name=db_patient.name,
        age=db_patient.age,
        diagnosis_stage=db_patient.diagnosis_stage,
        language_preference=db_patient.language_preference,
        cultural_background=db_patient.cultural_background,
        created_at=db_patient.created_at,
        updated_at=db_patient.updated_at
    )

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get patient by ID"""
    
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return PatientResponse(
        id=patient.id,
        name=patient.name,
        age=patient.age,
        diagnosis_stage=patient.diagnosis_stage,
        language_preference=patient.language_preference,
        cultural_background=patient.cultural_background,
        created_at=patient.created_at,
        updated_at=patient.updated_at
    )

@router.get("/", response_model=List[PatientResponse])
async def list_patients(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all patients"""
    
    result = await db.execute(
        select(Patient)
        .offset(skip)
        .limit(limit)
        .order_by(Patient.created_at.desc())
    )
    patients = result.scalars().all()
    
    return [
        PatientResponse(
            id=patient.id,
            name=patient.name,
            age=patient.age,
            diagnosis_stage=patient.diagnosis_stage,
            language_preference=patient.language_preference,
            cultural_background=patient.cultural_background,
            created_at=patient.created_at,
            updated_at=patient.updated_at
        )
        for patient in patients
    ]

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update patient information"""
    
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update fields if provided
    update_data = patient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    await db.commit()
    await db.refresh(patient)
    
    return PatientResponse(
        id=patient.id,
        name=patient.name,
        age=patient.age,
        diagnosis_stage=patient.diagnosis_stage,
        language_preference=patient.language_preference,
        cultural_background=patient.cultural_background,
        created_at=patient.created_at,
        updated_at=patient.updated_at
    )

@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a patient"""
    
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    await db.delete(patient)
    await db.commit()
    
    return {"message": "Patient deleted successfully"}
