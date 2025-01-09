from dotenv import load_dotenv
from agents.news_reader import create_rosetta_news_crew
import os
import warnings

load_dotenv()

# Required environment variables
REQUIRED_ENV_VARS = [
    "DEEPSEEK_API_KEY",
    "SERPER_API_KEY"
]

# Validate environment variables
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Configuration
OPENAI_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_BASE = 'https://api.deepseek.com'
OPENAI_MODEL_NAME = "deepseek-chat"
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Suppress warnings
warnings.filterwarnings('ignore')

crew = create_rosetta_news_crew(url="https://www.deepika.com/LatestNews.aspx", language="English")
    
inputs = {
    "url" : "https://www.deepika.com/LatestNews.aspx", 
    "language":"English"
}
result = crew.kickoff(inputs=inputs)

print(result.raw)




