from dotenv import load_dotenv
from agents.news_reader import create_rosetta_news_crew
from Gateway.emailGateway import EmailGateway
import os
import warnings
import logging
import time

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

# Medical news source - focusing on most reliable source
MEDICAL_NEWS_SOURCE = "https://www.news-medical.net/medical"

def process_medical_news() -> str:
    """
    Process medical news from the specified source.
    
    Returns:
        str: Processed news content
    """
    try:
        logger.info(f"Processing news from: {MEDICAL_NEWS_SOURCE}")
        crew = create_rosetta_news_crew(url=MEDICAL_NEWS_SOURCE, language="English")
        result = crew.kickoff()
        logger.info("Successfully processed medical news")
        return result.raw
    except Exception as e:
        logger.error(f"Error processing medical news: {str(e)}")
        raise

def main():
    try:
        # Check environment variables
        missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

        # Setup email configuration
        RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')
        if not RECIPIENTS or not all(RECIPIENTS):
            raise EnvironmentError("EMAIL_RECIPIENTS environment variable is missing or empty")

        email_gateway = EmailGateway(
            api_key=os.getenv('RESEND_API_KEY'),
            recipients=RECIPIENTS
        )

        # Process news
        start_time = time.time()
        logger.info("Starting medical news processing")
        
        news_content = process_medical_news()
        
        if not news_content:
            raise ValueError("No news content was successfully processed")

        # Send email
        logger.info("Sending email digest")
        result = email_gateway._run(news_content)
        if "Failed" in result:
            raise RuntimeError("Failed to send email")
        
        end_time = time.time()
        logger.info(f"News digest sent successfully! Processing time: {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    main()