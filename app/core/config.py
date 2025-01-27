from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Kakao Channel Settings
    KAKAO_CHANNEL_ID: str
    KAKAO_API_KEY: str
    KAKAO_CHANNEL_SECRET: str
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./korail_bot.db"
    
    # Redis Settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Encryption Settings
    ENCRYPTION_KEY: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
