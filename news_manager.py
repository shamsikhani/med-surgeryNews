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
    required_vars = ['SERPER_API_KEY', 'OPENAI_API_KEY', 'RESEND_API_KEY', 'EMAIL_RECIPIENTS']
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")

def get_category_sources(category):
    """Get sources for a specific category"""
    if category not in NEWS_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    
    category_data = NEWS_CATEGORIES[category]
    return category_data['sources']

def get_category_queries(category):
    """Get search queries for a specific category"""
    if category not in NEWS_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    
    category_data = NEWS_CATEGORIES[category]
    return category_data['queries']

def process_medical_news(category):
    """Process medical news for a specific category"""
    try:
        sources = get_category_sources(category)
        queries = get_category_queries(category)
        
        # Initialize the news reader agent
        news_reader = NewsReaderAgent()
        
        # Process each query
        all_news = []
        for query in queries:
            for source in sources:
                try:
                    news = news_reader.search_news(query, source)
                    if news:
                        all_news.extend(news)
                except Exception as e:
                    logger.error(f"Error processing source {source} with query {query}: {str(e)}")
                    continue
        
        # Remove duplicates based on title
        unique_news = []
        seen_titles = set()
        for news in all_news:
            if news['title'] not in seen_titles:
                unique_news.append(news)
                seen_titles.add(news['title'])
        
        # Sort by date (if available)
        unique_news.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return unique_news
        
    except Exception as e:
        logger.error(f"Error processing {category} news: {str(e)}")
        raise

def send_news_email(news_content):
    """Send news content via email"""
    try:
        # Format news content for email
        email_body = "# Latest Medical AI News\n\n"
        for news in news_content:
            email_body += f"## {news['title']}\n"
            email_body += f"{news['snippet']}\n"
            if 'link' in news:
                email_body += f"[Read more]({news['link']})\n"
            email_body += "\n---\n\n"
        
        # Send email using the email agent
        news_reader = NewsReaderAgent()
        news_reader.send_email(email_body)
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise

def main():
    """Main function"""
    try:
        # Set up argument parser
        parser = argparse.ArgumentParser(description='Medical News Aggregator')
        parser.add_argument('--category', 
                          choices=list(NEWS_CATEGORIES.keys()),
                          help='Category of medical news to process')
        args = parser.parse_args()
        
        # Load environment variables
        load_environment()
        
        # If no category specified, show available categories
        if not args.category:
            print("Available categories:")
            for category in NEWS_CATEGORIES:
                print(f"- {category}")
            return
        
        # Process news and send email
        news_content = process_medical_news(args.category)
        if news_content:
            send_news_email(news_content)
            print(f"Successfully processed and sent {args.category} news")
        else:
            print(f"No news found for category: {args.category}")
            
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()