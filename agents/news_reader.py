from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

def create_press_bureau_agent(url: str, language: str) -> Agent:
    return Agent(
        role="Press Bureau AI - Chief Intelligence Officer",
        goal=f"Scrape the news website homepage with URL {url}. This is a new portal in {language} language."
            "Get the top 10 headlines, navigate to the detailed news articles under each headline"
            " and summarize the news articles in English."
            "You perform story importance assessment using established news values."
            "The headlines from the main section of the page will be prioritized"
            "You will generate wire service-style bulletins",
        backstory="You are a sophisticated press bureau agent, specializing in global news monitoring and synthesis."
            "The news website could be in any language. "
            "You will translate the news articles into English. "
            "You will also provide a summary of the news articles in English. "
            "Expert in AP/Reuters style guides, multi-language news analysis, and editorial standards."
            "You are trained on decades of journalistic best practices from leading wire services and newspapers."
            "All of the content generated should be based on the news articles, make no assumptions.",
        verbose=True,
        allow_delegation=False,
    )

def create_editor_agent() -> Agent:
    return Agent(
        role="Editor-in-Chief",
        goal="You will make sure the article maintains consistent editorial tone and voice"
            "You will check the article for libel and defamation"
            "You will review story priority rankings"
            "You will verify headline accuracy and impact"
            "The headlines from the main section of the page will be prioritized"
            "You will gcross check translation accuracy",
        backstory="A seasoned editorial AI agent with deep expertise in journalistic standards, fact-checking protocols,"
            " and multi-language content verification. Trained in editorial practices of leading international news organizations."
            "You are trained on decades of journalistic best practices from leading wire services and newspapers."
            "You review the news articles submitted by the Press Bureau AI and provide feedback on the quality of the content."
            "You will perform libel and defamation checks on the news articles."
            "You will enforce AP/Reuters style guidelines and editorial standards."
            "You will make sure journalistic ethics are upheld and the content is factually accurate."
            "You will make sure the content is not biased and is fair and balanced."
            "You will make sure the content is not misleading and is clear and concise."
            "You will make sure the content is not offensive and is appropriate for a global audience."
            "You will make sure the content is not sensational and is based on news values.",
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
                        "1. Prioritize the latest news from website {url}. Read complete news articles and summarize them in English.\n"
                        "2. Develop a detailed content outline including "
                            "an introduction, key points, summary.\n"
                        "3. Include relevant data or sources.\n"
                        "4. If required, you may perform additional search on the topic for better context understanding.\n"
                        "5. Add reference to the original news articles.\n"
                    ),
                    expected_output="A list of comprehensive news articles translated in English from the website {url} "
                        "using AP/Reuters style guides and unbiased tone.",
                        tools=[search_tool, scrape_tool, global_scrape_tool],
                        agent=press_bureau_agent,
                    )   

    editor_task = Task(
                        description="1. Review the news articles and provide feedback on the quality of the content.\n"
                        "2. Make sure the content is not biased and is fair and balanced.\n"
                        "3. Make sure the content is not misleading and is clear and concise.\n"
                        "4. Make sure the content is not offensive and is appropriate for a global audience.\n"
                        "5. Make sure the content is not sensational and is based on news values.\n",
                        expected_output="A well-written list of news articles "
                                        "in markdown format, ready for publication, "
                                        "each news article should not exceed more than 2 or 3 paragraphs.",
                        agent=editor_agent,
                    )   
    
    return Crew(
        agents=[press_bureau_agent, editor_agent],
        tasks=[bureau_task, editor_task],
    #    manager=manager,
        verbose=True,
        memory=False
    ) 