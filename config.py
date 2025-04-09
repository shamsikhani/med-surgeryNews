from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Keys
    SERPER_API_KEY: str
    RESEND_API_KEY: str
    OPENAI_API_KEY: str
    
    # OpenAI Configuration
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_MODEL_NAME: str = "gpt-4"
    
    # Email Configuration
    EMAIL_SUBJECT: str = "Daily Medical & Surgical News Digest"
    EMAIL_SENDER: str = "Medical News <onboarding@resend.dev>"
    EMAIL_RECIPIENTS: str
    
    # Medical news sources
    MEDICAL_NEWS_SOURCES: List[str] = [
        "https://www.medicalnewstoday.com/medical-news",
        "https://www.news-medical.net/medical",
        "https://www.sciencedaily.com/news/health_medicine/",
        "https://www.healthline.com/health-news"
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"