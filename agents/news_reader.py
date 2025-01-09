from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from typing import List, Optional

def create_press_bureau_agent(url: str, language: str) -> Agent:
    """Create a press bureau agent for news processing.
    
    Args:
        url (str): The URL of the news website to scrape
        language (str): The language of the news content
        
    Returns:
        Agent: Configured press bureau agent
    
    Raises:
        ValueError: If url or language is empty
    """
    if not url or not language:
        raise ValueError("URL and language must be provided")
    return Agent(
        role="Press Bureau AI - Chief Intelligence Officer",
        goal=f"Scrape the news website homepage with URL {url} and read complete news articles. "
            f"This is a news portal in {language} language. "
            "First get the top 10 headlines and their corresponding article URLs. "
            "Then visit each article URL to read the full article content. "
            "Summarize each complete article in English, maintaining the tone of the article. ",
        backstory="You are a sophisticated press bureau agent, specializing in global news monitoring and synthesis. "
            "For each headline you find, you will:"
            "1. Extract the article's URL "
            "2. Visit the full article page "
            "3. Read and comprehend the complete article content "
            "4. Translate the entire article to English "
            "5. Provide a comprehensive summary of 2-3 paragraphs "
            "Expert in AP/Reuters style guides, multi-language news analysis, and editorial standards. "
            "All content generated should be based on the complete articles, not just headlines.",
        verbose=True,
        allow_delegation=False,
    )

def create_editor_agent() -> Agent:
    return Agent(
        role="Editor-in-Chief",
        goal="You will make sure the article maintains consistent editorial tone and voice"
#            "You will check the article for libel and defamation"
            "You will review story priority rankings"
 #           "You will verify headline accuracy and impact"
            "You will double check translation accuracy",
        backstory="A seasoned editorial AI agent with deep expertise in journalistic standards"
#            ", fact-checking protocols,"
            " and multi-language content verification. Trained in editorial practices of leading international news organizations."
            "You are trained on decades of journalistic best practices from leading wire services and newspapers."
            "You review the news articles submitted by the Press Bureau AI and provide feedback on the quality of the content."
#            "You will perform libel and defamation checks on the news articles."
            "You will enforce AP/Reuters style guidelines and editorial standards."
 #           "You will make sure journalistic ethics are upheld and the content is factually accurate."
            "You will make sure the content is not biased and is fair and balanced."
#            "You will make sure the content is not misleading and is clear and concise."
            "You will make sure the content is not offensive and is appropriate for a global audience."
            "You will make sure the content aligns with journalistic values.",
        verbose=True,
        allow_delegation=True,
    )

def create_rosetta_news_crew(url: str, language: str) -> Crew:
    """
    Create a crew of news agents to read news articles and generate wire service-style bulletins
    """
    press_bureau_agent = create_press_bureau_agent(url, language)
    editor_agent = create_editor_agent()

    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool(url=url)
    global_scrape_tool = ScrapeWebsiteTool()
    bureau_task = Task(
        description=(
            "1. Visit the news website link at: {url} and find 10 headlines. Each headline will have a URL. Use tools at your disposal to access each URL's content and fetch detailed news for the article.\n"
            "2. Generate headline and 2-3 paragraph summary of the article content in English. Article URL is optional.\n"
            "3. Do not show any clear indication in the generated article that you are summarizing the original article (for example, starting the article with the "
            "phrase 'This article explores' or similar. miantain the tone of the original article.\n"
            "4. Format output in markdown with clear separation between articles.\n"
        ),
        expected_output="A list of 10 comprehensive article summaries in English, "
            "formatted as an email-friendly markdown document with proper spacing and structure.",
        tools=[search_tool, scrape_tool, global_scrape_tool],
        agent=press_bureau_agent,
    )   

    editor_task = Task(
                        description="1. Review the news articles and provide feedback on the quality of the content.\n"
                        "2. Make sure the content is not biased and is fair and balanced.\n"
#                        "3. Make sure the content is not misleading and is clear and concise.\n"
                        "3. Make sure the content is not offensive and is appropriate for a global audience.\n"
                        "4. Use neutral tone and language.\n"
                        "5. Make sure article URL is included in the response.\n",
                        expected_output="A well-written list of news articles "
                                        "in markdown format, ready for publication, ",
#                                        "each news article should not exceed more than 2 or 3 paragraphs.",
                        agent=editor_agent,
                    )   
    
    return Crew(
        agents=[press_bureau_agent, editor_agent],
        tasks=[bureau_task, editor_task],
    #    manager=manager,
        verbose=True,
        memory=False
    ) 

