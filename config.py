from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_MODEL_NAME: str = "gpt-4"
    
    # Medical news sources
    MEDICAL_NEWS_SOURCES: List[str] = [
        "https://www.medicalnewstoday.com/medical-news",
        "https://www.news-medical.net/medical",
        "https://www.sciencedaily.com/news/health_medicine/",
        "https://www.healthline.com/health-news"
    ]
    
    # Email configuration
    EMAIL_SUBJECT: str = "Daily Medical & Surgical News Digest"
    EMAIL_SENDER: str = "Rosetta Medical News <onboarding@resend.dev>"
    
    class Config:
        env_file = ".env"