"""
Configuration settings for Faker backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Keys
    GOOGLE_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "postgresql://faker_user:faker_password@localhost:5432/faker_alzheimer"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React Native dev
        "http://localhost:19006", # Expo web
        "http://localhost:8080",  # Dashboard
    ]
    
    # Gemma 3n Settings
    GEMMA_MODEL: str = "gemma-3-27b-it"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    
    # Audio Settings
    MAX_AUDIO_SIZE_MB: int = 10
    SUPPORTED_AUDIO_FORMATS: List[str] = ["wav", "mp3", "m4a", "ogg"]
    
    # Image Settings
    MAX_IMAGE_SIZE_MB: int = 5
    SUPPORTED_IMAGE_FORMATS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
