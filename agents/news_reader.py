from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import sys
import codecs
import logging
import traceback
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set UTF-8 as default encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_press_bureau_agent(urls: List[str], language: str) -> Agent:
    try:
        if not urls or not language:
            raise ValueError("URLs and language must be provided")
        logger.info(f"Creating press bureau agent for URLs: {urls}")
        
        tools = [
            SerperDevTool(),
            ScrapeWebsiteTool()
        ]
        
        return Agent(
            role="Medical Press Bureau AI",
            goal="Extract and summarize the latest medical news articles from multiple sources",
            backstory="Expert in medical news curation and summarization, specializing in healthcare developments. Capable of analyzing multiple sources to identify the most significant developments.",
            tools=tools,
            verbose=True
        )
    except Exception as e:
        logger.error(f"Error creating press bureau agent: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def create_editor_agent() -> Agent:
    return Agent(
        role="Medical Editor",
        goal="Review and enhance medical content for accuracy and clarity",
        backstory="Expert medical editor with extensive experience in healthcare communications",
        verbose=True
    )

def create_medical_expert_agent() -> Agent:
    return Agent(
        role="Medical Expert Reviewer",
        goal="Ensure medical accuracy and provide clinical context",
        backstory="Board-certified physician with expertise in medical research and clinical practice",
        verbose=True
    )

def create_rosetta_news_crew(urls: List[str], language: str = "English") -> Crew:
    try:
        press_bureau = create_press_bureau_agent(urls=urls, language=language)
        logger.info("Creating editor agent")
        editor = create_editor_agent()
        logger.info("Creating medical expert agent")
        medical_expert = create_medical_expert_agent()
        
        bureau_task = Task(
            description=f"""
            1. Search through all provided medical news sources: {', '.join(urls)}
            2. Collect and analyze medical news articles from each source
            3. Compare and evaluate the importance of articles across all sources
            4. Select and summarize the top 5 most significant medical news articles
            5. Format the summaries in markdown with clear headers and source attribution
            """,
            expected_output="A list of 5 most significant medical article summaries in markdown format, selected from all sources",
            agent=press_bureau
        )
        
        expert_task = Task(
            description="Review the medical content for accuracy and add clinical context",
            expected_output="Reviewed and enhanced medical articles with clinical context",
            agent=medical_expert
        )
        
        editor_task = Task(
            description="Polish the content for clarity while maintaining medical accuracy",
            expected_output="Final polished medical news digest ready for distribution",
            agent=editor
        )
        
        logger.info("Creating crew")
        return Crew(
            agents=[press_bureau, medical_expert, editor],
            tasks=[bureau_task, expert_task, editor_task],
            verbose=True
        )
    except Exception as e:
        logger.error(f"Error creating crew: {str(e)}")
        logger.error(traceback.format_exc())
        raise
