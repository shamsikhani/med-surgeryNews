from dotenv import load_dotenv
from agents.news_reader import create_rosetta_news_crew
from Gateway.emailGateway import EmailGateway
from config import Settings
import os
import warnings
import logging
import time
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Required environment variables
REQUIRED_ENV_VARS = [
    "SERPER_API_KEY",
    "RESEND_API_KEY",
    "OPENAI_API_KEY"
]

def check_env_vars():
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def main():
    try:
        # Check environment variables
        check_env_vars()
        
        # Load settings
        settings = Settings()
        
        # Create and run the news crew with all sources
        logger.info("Creating news crew with multiple sources")
        crew = create_rosetta_news_crew(
            urls=settings.MEDICAL_NEWS_SOURCES,
            language="English"
        )
        
        # Run the crew tasks
        logger.info("Starting crew tasks")
        crew_output = crew.kickoff()
        news_digest = str(crew_output)  # Convert CrewOutput to string
        
        # Initialize email gateway
        logger.info("Initializing email gateway")
        recipients = settings.EMAIL_RECIPIENTS.split(",")
        email_gateway = EmailGateway(
            api_key=settings.RESEND_API_KEY,
            recipients=recipients
        )
        
        # Send the news digest
        logger.info("Sending news digest")
        success = email_gateway.send_email(
            markdown_content=news_digest,
            subject=settings.EMAIL_SUBJECT
        )
        
        if success:
            logger.info("News digest sent successfully")
        else:
            logger.error("Failed to send news digest")
            
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    main()