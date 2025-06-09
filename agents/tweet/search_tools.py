import os
from crewai import Agent, Task, Crew
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    ScrapeElementFromWebsiteTool,
    ScrapeWebsiteTool
)
from browser_tools import WebsiteSummarizerTool
from dotenv import load_dotenv
load_dotenv()

# Set environment variables
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if SERPER_API_KEY is not None:
    os.environ["SERPER_API_KEY"] = SERPER_API_KEY
if OPENAI_API_KEY is not None:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize tools
search_tool = SerperDevTool()
website_tool = WebsiteSearchTool()
element_scraper = ScrapeElementFromWebsiteTool()
scrape_website_tool = ScrapeWebsiteTool()
summarizer_tool = WebsiteSummarizerTool()

# Shared Agent Definition
Content_Creator = Agent(
    role='TWITTER POST WRITER',
    goal='To find accurate and relevant information on the web according for a given topic and user for twitter posts',
    backstory='You are a highly skilled web researcher and content creator, adept at finding and summarizing information from various online sources to create engaging Twitter posts.',
    tools=[search_tool, website_tool, element_scraper, scrape_website_tool, summarizer_tool],
    llm='gpt-4o',
    verbose=True
)


def Content_Search(topic: str, user_profile: dict) -> str:
    """Performs a research for creating a Twitter post based on the provided topic and user profile."""
    task = Task(
        description=f"Conduct a deep search for creating a twitter post about the the topic : {topic} \n and for user profile : {user_profile}\n\nAnd tweet should be less than 250 characters.",
        expected_output='A Engaging Twitter post in 2-3 sentences without hastags or links, that is informative, entertaining, and aligned with the user profile.',
        agent=Content_Creator,
        tools=[search_tool, website_tool, element_scraper, scrape_website_tool, summarizer_tool],
    )
    crew = Crew(agents=[Content_Creator], tasks=[task], verbose=False, planning=True)
    result = crew.kickoff()
    return str(result)