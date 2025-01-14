import argparse
import logging
import os
from config.news_sources import NEWS_CATEGORIES
from agents.news_reader import NewsReaderAgent
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(process)d - %(name)s:%(lineno)d - %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_environment():
    """Load environment variables"""
    load_dotenv()
    required_vars = [
        'SERPER_API_KEY',
        'OPENAI_API_KEY',
        'RESEND_API_KEY',
        'EMAIL_RECIPIENTS'
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")

def get_category_sources(category):
    """Get sources for a specific category"""
    if category not in NEWS_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    return NEWS_CATEGORIES[category]['sources']

def get_category_queries(category):
    """Get search queries for a specific category"""
    if category not in NEWS_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    return NEWS_CATEGORIES[category]['queries']

def process_medical_news(category):
    """
    Process medical news for a specific category.
    NOTE: This will send one email per category, containing up to 5 articles total 
    for that category (taken from all queries and sources).
    """
    try:
        sources = get_category_sources(category)
        queries = get_category_queries(category)

        # Initialize the news reader agent
        news_reader = NewsReaderAgent()

        all_news = []
        for query in queries:
            for source in sources:
                # Each call returns up to 5 articles
                news_items = news_reader.search_news(query, source)
                all_news.extend(news_items)

        # Now we have a combined list (could be more than 5 total).
        # But the final formatting also slices to 5 articles.
        if all_news:
            email_content = news_reader.format_email_content(all_news, category=category)
            if news_reader.send_email(email_content):
                print(f"\nSuccessfully processed and sent {category} news")
            else:
                print(f"\nFailed to send {category} news email")
        else:
            print(f"\nNo news found for {category}")

    except Exception as e:
        logger.error(f"Error processing {category} news: {str(e)}", exc_info=True)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Process medical AI news')
    parser.add_argument(
        '--category',
        type=str,
        choices=NEWS_CATEGORIES.keys(),
        help='Category of medical news to process'
    )
    args = parser.parse_args()

    try:
        # Load environment variables
        load_environment()

        if args.category:
            # Process news for the specified category only
            process_medical_news(args.category)
        else:
            # Process all categories if none specified
            for cat in NEWS_CATEGORIES.keys():
                process_medical_news(cat)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        return 1

    return 0

if __name__ == "__main__":
    main()
