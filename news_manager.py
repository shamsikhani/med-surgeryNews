from dotenv import load_dotenv
from agents.news_reader import create_rosetta_news_crew
from Gateway.emailGateway import EmailGateway
import os
import warnings

load_dotenv()

# Required environment variables
REQUIRED_ENV_VARS = [
    "SERPER_API_KEY",
    "RESEND_API_KEY",
    "OPENAI_API_KEY"
]

url = "https://www.manoramaonline.com/news/latest-news.html"

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')
if not RECIPIENTS or not all(RECIPIENTS):
    raise EnvironmentError("EMAIL_RECIPIENTS environment variable is missing or empty")

email_gateway = EmailGateway(api_key=os.getenv('RESEND_API_KEY'), recipients=RECIPIENTS)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = 'https://api.openai.com/v1'
OPENAI_MODEL_NAME = "gpt-4o"
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

warnings.filterwarnings('ignore')
# Create and run crew

crew = create_rosetta_news_crew(url=url, language="English")
inputs={    
    "url": url, 
    "language": "English"
}
result = crew.kickoff(inputs=inputs)
# Send email with results
print(result.raw)
email_gateway.send_email(result.raw)
print("News digest sent via email!")