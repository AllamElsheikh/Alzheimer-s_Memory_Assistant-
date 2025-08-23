"""
Faker - Alzheimer's Memory Assistant Backend
FastAPI application with Gemma 3n integration
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
from contextlib import asynccontextmanager

from app.api import conversations, patients, assessments, reminders
from app.core.config import settings
from app.services.gemma_service import GemmaService
from app.services.database import init_db

# Initialize security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await init_db()
    print("🚀 Faker Backend Started")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    print(f"🤖 Gemma 3n API: {'Enabled' if settings.GOOGLE_API_KEY else 'Disabled'}")
    
    yield
    
    # Shutdown
    print("👋 Faker Backend Shutting Down")

# Create FastAPI app
app = FastAPI(
    title="Faker - Alzheimer's Memory Assistant API",
    description="Evidence-based AI assistant for Arabic-speaking Alzheimer's patients",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["assessments"])
app.include_router(reminders.router, prefix="/api/v1/reminders", tags=["reminders"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Faker - Alzheimer's Memory Assistant API",
        "version": "1.0.0",
        "status": "healthy",
        "gemma_available": bool(settings.GOOGLE_API_KEY)
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    gemma_service = GemmaService()
    
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "gemma_api": "available" if await gemma_service.test_connection() else "unavailable",
            "redis": "connected"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
