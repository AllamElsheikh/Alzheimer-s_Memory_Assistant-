"""
Database models for Faker - Alzheimer's Memory Assistant
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()

class Patient(Base):
    """Patient model"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    diagnosis_stage = Column(String(50))  # early, moderate, severe
    language_preference = Column(String(10), default="ar")
    cultural_background = Column(String(50))
    emergency_contacts = Column(JSON)
    medication_schedule = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    conversations = relationship("Conversation", back_populates="patient")
    memories = relationship("Memory", back_populates="patient")
    assessments = relationship("Assessment", back_populates="patient")
    reminders = relationship("Reminder", back_populates="patient")

class Conversation(Base):
    """Conversation model"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    session_id = Column(String(100), index=True)
    content = Column(Text, nullable=False)
    response = Column(Text)
    audio_path = Column(String(255))
    image_path = Column(String(255))
    mood_score = Column(Float)
    cognitive_score = Column(Float)
    interaction_type = Column(String(50))  # text, voice, image, multimodal
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="conversations")

class Memory(Base):
    """Memory model for storing patient memories and associations"""
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    content = Column(Text, nullable=False)
    media_type = Column(String(20))  # text, image, audio, video
    media_path = Column(String(255))
    importance_score = Column(Float, default=0.5)
    tags = Column(JSON)
    last_accessed = Column(DateTime(timezone=True))
    access_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="memories")

class Assessment(Base):
    """Cognitive assessment model"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    assessment_type = Column(String(50), nullable=False)  # memory, attention, language, executive
    scores = Column(JSON)  # Detailed scores for different cognitive domains
    severity_level = Column(String(20))  # normal, mild, moderate, severe
    recommendations = Column(JSON)
    raw_data = Column(JSON)  # Raw assessment data
    administered_by = Column(String(100))  # AI, caregiver, clinician
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="assessments")

class Reminder(Base):
    """Reminder model"""
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    reminder_type = Column(String(50))  # medication, appointment, activity, social
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(100))  # daily, weekly, monthly
    is_completed = Column(Boolean, default=False)
    completion_time = Column(DateTime(timezone=True))
    priority = Column(String(10), default="medium")  # low, medium, high, urgent
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="reminders")

class Caregiver(Base):
    """Caregiver model"""
    __tablename__ = "caregivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    relationship = Column(String(50))  # family, professional, friend
    is_primary = Column(Boolean, default=False)
    notification_preferences = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PatientCaregiver(Base):
    """Many-to-many relationship between patients and caregivers"""
    __tablename__ = "patient_caregivers"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=False)
    access_level = Column(String(20), default="view")  # view, manage, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    """Alert model for caregiver notifications"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"))
    alert_type = Column(String(50), nullable=False)  # emergency, medication, behavior, assessment
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
