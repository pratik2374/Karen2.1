import os
from crewai import Agent, Task, Crew
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    ScrapeElementFromWebsiteTool
)
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

# Shared Agent Definition
search_agent = Agent(
    role='Web Intelligence Agent',
    goal='Extract accurate, relevant insights from the web based on user queries',
    backstory='An expert in online research and summarization, capable of answering quick prompts and long-form inquiries using multiple tools.',
    tools=[search_tool, website_tool, element_scraper],
    verbose=True
)

# === 1. Deep Search ===
def deep_search(query: str, output_file: str = "deep_search_result.md"):
    """Performs an in-depth 4–5 paragraph search and saves the result to a markdown file."""
    task = Task(
        description=f"Conduct a deep web search for: \"{query}\" and generate a detailed summary in 4–5 paragraphs in markdown format.",
        expected_output='Markdown-formatted detailed summary covering background, current facts, and future projections.',
        agent=search_agent,
        output_file=output_file
    )
    crew = Crew(agents=[search_agent], tasks=[task], verbose=True, planning=True)
    result = crew.kickoff()
    print(f"✅ Deep search completed and saved to: {output_file}")
    return result


# === 2. Quick Search ===
def quick_search(query: str) -> str:
    """Returns a medium-depth 3–4 paragraph search summary directly as a string."""
    task = Task(
        description=f"Perform a quick search for: \"{query}\" and summarize the key points in 3–4 informative paragraphs.",
        expected_output='Concise summary in 3–4 paragraphs highlighting main takeaways.',
        agent=search_agent,
    )
    crew = Crew(agents=[search_agent], tasks=[task], verbose=False, planning=True)
    result = crew.kickoff()
    return str(result)


# === 3. Instant Answer ===
def instant_answer(query: str) -> str:
    """Returns a 1–2 line summary/definition/fact quickly."""
    task = Task(
        description=f"Provide a quick one-liner answer or definition for: \"{query}\".",
        expected_output='1–2 line direct response or fact.',
        agent=search_agent,
    )
    crew = Crew(agents=[search_agent], tasks=[task], verbose=False, planning=False)
    result = crew.kickoff()
    return str(result)


# === Sample Usage ===
if __name__ == "__main__":
    # Deep Search Example
    deep_search("Impact of Generative AI on future job markets", output_file="ai_jobs_impact.md")

    # Quick Search Example
    result = quick_search("Top 3 LLM models released in 2025")
    print("\n=== Quick Search Result ===\n")
    print(result)

    # Instant Answer Example
    answer = instant_answer("What is AGI?")
    print("\n=== Instant Answer ===\n")
    print(answer)