from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_MODEL_NAME: str = "gpt-4"
    NEWS_URL: str = "https://www.manoramaonline.com/news/latest-news.html"
    
    class Config:
        env_file = ".env" 