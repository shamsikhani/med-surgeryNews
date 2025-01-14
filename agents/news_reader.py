import os
import logging
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import resend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(process)d - %(filename)s-%(module)s:%(lineno)d - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class NewsReaderAgent:
    def __init__(self):
        """Initialize the NewsReaderAgent"""
        load_dotenv()
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.resend_api_key = os.getenv('RESEND_API_KEY')

        # Parse recipients from environment (comma-separated)
        env_recipients = os.getenv('EMAIL_RECIPIENTS', '')
        self.email_recipients = [r.strip() for r in env_recipients.split(',') if r.strip()]

    def search_news(self, query, source):
        """Search for news articles and generate reader-friendly summaries."""
        try:
            logging.info(f"Starting news search - Query: '{query}', Source: '{source}'")

            # Create the search agent
            logging.info("Creating search agent...")
            search_agent = Agent(
                role='Medical News Researcher',
                goal='Find and summarize the latest medical AI news in a way that is easy for doctors to understand',
                backstory='I am an AI assistant specialized in making complex medical technology news accessible to healthcare professionals. I provide detailed, comprehensive summaries that capture the full context and implications of each article.',
                tools=[SerperDevTool()]
            )
            logging.info("Search agent created successfully")

            # Create the research task with strict formatting requirements
            logging.info("Creating research task...")
            search_task = Task(
                description=f'''Search for "{query}" from {source} and create detailed summaries. Format EXACTLY as follows:

TITLE: [Full Article Title Without Any Truncation]
URL: [Article URL]
SUMMARY: [A comprehensive paragraph summary (150-200 words) that covers:
- Main findings or technological advancement
- Methodology or approach used
- Key benefits and potential impact
- Important results or validation data
- Practical implications for healthcare professionals]

Important:
1. Start each article with TITLE: on a new line
2. Follow with URL: on the next line
3. End with SUMMARY: on the next line
4. Add a blank line between articles
5. Do not use any other formatting (no ##, ###, etc.)
6. Do not add any other text or sections
7. Ensure summaries are detailed and comprehensive
8. Keep the complete article title, do not truncate

Example of exact format:

TITLE: Novel Deep Learning Algorithm Demonstrates 98% Accuracy in Early Detection of Lung Nodules from Standard Chest X-rays
URL: https://example.com/article1
SUMMARY: This groundbreaking study introduces a sophisticated deep learning algorithm that has achieved remarkable accuracy in detecting early-stage lung nodules from standard chest X-rays. The research team, led by Dr. Sarah Chen at Stanford Medical Center, developed and validated the algorithm using a diverse dataset of over 100,000 chest X-rays from multiple institutions. The AI system demonstrated a sensitivity of 98% and specificity of 96%, significantly outperforming traditional computer-aided detection systems and matching the accuracy of experienced radiologists. The algorithm's unique architecture incorporates attention mechanisms and multi-scale feature analysis, enabling it to detect nodules as small as 3mm while maintaining a low false-positive rate. Validation studies across different patient populations and imaging equipment showed consistent performance, suggesting robust real-world applicability. This advancement could substantially improve early lung cancer detection, particularly in resource-limited settings where expert radiologists may not be readily available.

TITLE: Integration of Artificial Intelligence with Picture Archiving and Communication Systems (PACS) Streamlines Radiological Workflow
URL: https://example.com/article2
SUMMARY: A comprehensive implementation study reveals how the integration of AI tools within existing PACS infrastructure has revolutionized radiological workflows at major medical centers. The research, conducted over 18 months across five teaching hospitals, demonstrates a 40% reduction in report turnaround time and a 35% increase in radiologist productivity. The integrated system uses machine learning algorithms to prioritize urgent cases, automatically detect common abnormalities, and provide structured reporting templates. Notably, the AI system's natural language processing capabilities help standardize reporting while maintaining flexibility for radiologist input. The implementation resulted in improved emergency department response times and better communication between radiologists and referring physicians. Cost-benefit analysis showed a return on investment within 14 months, making this solution particularly attractive for medium to large healthcare facilities.
''',
                expected_output="A list of articles with complete titles, URLs, and detailed paragraph summaries in the exact specified format",
                agent=search_agent
            )
            logging.info("Research task created successfully")

            # Create and execute the crew
            logging.info("Creating crew for task execution...")
            crew = Crew(
                agents=[search_agent],
                tasks=[search_task],
                process=Process.sequential,
                verbose=True
            )
            logging.info("Crew created successfully")

            logging.info("Starting search task execution...")
            result = crew.kickoff()
            logging.info("Search task execution completed")

            if not result or not result.raw:
                logging.warning("No results returned from the search")
                return []

            # Process the results
            logging.info("Processing search results...")
            articles = []
            current_article = {}

            for line in result.raw.split('\n'):
                line = line.strip()
                if not line:
                    # blank line -> we finalize the current article (if any)
                    if current_article:
                        articles.append(current_article)
                        current_article = {}
                    continue

                if line.startswith('TITLE: '):
                    # If there's an article in progress, push it to the list first
                    if current_article:
                        articles.append(current_article)
                    current_article = {'title': line[7:].strip()}

                elif line.startswith('URL: '):
                    current_article['link'] = line[5:].strip()

                elif line.startswith('SUMMARY: '):
                    current_article['snippet'] = line[9:].strip()

            # If there's a leftover article in progress, add it
            if current_article:
                articles.append(current_article)

            # Clean and validate articles
            logging.info("Cleaning and validating articles...")
            cleaned_articles = []
            for article in articles:
                if all(article.get(key) for key in ['title', 'link', 'snippet']):
                    cleaned_articles.append(article)
                    logging.info(f"Validated article: {article['title']}")
                else:
                    logging.warning(f"Skipped invalid article: {article.get('title', 'Unknown Title')}")

            logging.info(f"Found {len(cleaned_articles)} valid articles")
            # Limit to 5 right here:
            return cleaned_articles[:5]

        except Exception as e:
            logging.error(f"Error in search_news: {str(e)}", exc_info=True)
            return []

    def format_email_content(self, news_items, category=None):
        """Format news items into a simple, clean email."""
        logging.info("Starting email content formatting...")
        
        # Ensure we only take top 5 articles
        top_articles = news_items[:5]
        logging.info(f"Processing {len(top_articles)} articles for email")
        
        # Set category-specific title
        if category == 'radiology':
            email_title = 'Latest AI in Radiology Updates'
        elif category == 'surgery':
            email_title = 'Latest AI in Surgery Updates'
        elif category == 'medicine':
            email_title = 'Latest AI in Healthcare Updates'
        else:
            email_title = 'Latest Medical AI Updates'
        
        # Start with basic HTML structure
        email_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 20px;
                    line-height: 1.6;
                    color: #333;
                }}
                h1 {{
                    color: #2C3E50;
                    border-bottom: 2px solid #2C3E50;
                    padding-bottom: 10px;
                    margin-bottom: 30px;
                }}
                .article {{
                    background: #f9f9f9;
                    border-left: 4px solid #2C3E50;
                    padding: 20px;
                    margin-bottom: 25px;
                }}
                .article-title {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #2C3E50;
                    margin-bottom: 15px;
                    line-height: 1.4;
                }}
                .article-summary {{
                    margin: 15px 0;
                    text-align: justify;
                }}
                .article-link {{
                    color: #3498DB;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 10px;
                }}
                .article-link:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <h1>{email_title}</h1>
        """

        # Add each article block
        for article in top_articles:
            title = article.get('title', '').strip()
            url = article.get('link', '').strip()
            summary = article.get('snippet', '').strip()
            email_content += f"""
            <div class="article">
                <div class="article-title">{title}</div>
                <div class="article-summary">{summary}</div>
                <a href="{url}" class="article-link">Read Full Article →</a>
            </div>
            """

        email_content += """\
        </body>
        </html>
        """

        # Log a brief preview
        logging.info(f"Email HTML preview:\n{email_content[:500]}...")
        return email_content

    def send_email(self, html_content):
        """Send the email via Resend."""
        try:
            logging.info("Starting email preparation...")

            # Confirm the API key
            api_key = self.resend_api_key
            if not api_key:
                raise ValueError("RESEND_API_KEY environment variable not set")

            # Confirm we have recipients
            if not self.email_recipients:
                raise ValueError("EMAIL_RECIPIENTS environment variable not set or empty")

            logging.info(f"Recipients: {self.email_recipients}")

            # Initialize Resend
            resend.api_key = api_key

            # Build the params
            params = {
                "from": "Medical AI News <onboarding@resend.dev>",
                "to": self.email_recipients,  # Use the list properly
                "subject": "Latest Medical AI News Update",
                "html": html_content
            }

            # Debug logging
            logging.info("Sending email now...")
            logging.info(f"Email content preview (first 500 chars): {html_content[:500]}...")

            # Send the email
            response = resend.Emails.send(params)

            if response:
                logging.info(f"Email sent successfully. Response: {response}")
                return True
            else:
                raise Exception("Failed to send email - no response received")

        except Exception as e:
            logging.error(f"Error sending email: {str(e)}", exc_info=True)
            return False
