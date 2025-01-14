import os
import logging
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import markdown2
import resend

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(process)d - %(name)s:%(lineno)d - %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class NewsReaderAgent:
    def __init__(self):
        """Initialize the NewsReaderAgent"""
        load_dotenv()
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.resend_api_key = os.getenv('RESEND_API_KEY')
        self.email_recipients = os.getenv('EMAIL_RECIPIENTS', '').split(',')

    def search_news(self, query, source):
        """Search for news using the specified query and source"""
        try:
            # Create the search tool
            search_tool = SerperDevTool()

            # Create the search agent
            search_agent = Agent(
                role='Search Agent',
                goal='Find relevant medical AI news articles',
                backstory='Expert at finding and analyzing medical news articles',
                tools=[search_tool],
                verbose=True,
                allow_delegation=False
            )

            # Create the research task
            search_task = Task(
                description=f'Search for "{query}" from {source} and summarize the findings. Format each article as:\n# Title\nSummary\nURL',
                expected_output="A list of articles with titles, summaries, and URLs in markdown format",
                agent=search_agent
            )

            # Create and run the crew
            crew = Crew(
                agents=[search_agent],
                tasks=[search_task],
                process=Process.sequential,
                verbose=True
            )

            # Execute the search
            result = crew.kickoff()
            
            # Process the results into a structured format
            if result and result.raw:
                # Parse the raw results into a list of news items
                news_items = []
                current_item = None
                
                for line in result.raw.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith('# '):
                        if current_item:
                            news_items.append(current_item)
                        current_title = line[2:].strip()
                        current_item = {
                            'title': current_title,
                            'snippet': '',
                            'link': '',
                            'source': source
                        }
                    elif line.startswith('http'):
                        if current_item:
                            current_item['link'] = line.strip()
                    elif current_item:
                        current_item['snippet'] += line + ' '
                
                if current_item:
                    news_items.append(current_item)

                return news_items
            return []

        except Exception as e:
            logger.error(f"Error in search_news: {str(e)}")
            return []

    def send_email(self, content):
        """Send email with the news content"""
        try:
            if not self.resend_api_key:
                raise ValueError("Missing Resend API key")
            if not self.email_recipients:
                raise ValueError("No email recipients specified")

            # Convert markdown to HTML
            html_content = markdown2.markdown(content)

            # Initialize Resend
            resend.api_key = self.resend_api_key

            # Send email
            response = resend.Emails.send({
                "from": "Medical News Digest <onboarding@resend.dev>",
                "to": self.email_recipients,
                "subject": "Latest Medical AI News Update",
                "html": html_content
            })

            if response:
                logger.info("Email sent successfully")
                return "Email sent successfully"
            else:
                raise Exception("Failed to send email")

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            raise
