# src/web_scraper_ai/tools/website_summarizer.py

import os
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from typing import Type
from dotenv import load_dotenv
import openai

from crewai.tools import BaseTool

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Input schema
class WebsiteInput(BaseModel):
    url: str = Field(..., description="Full URL of the website (e.g., https://clearbit.com/about-us)")

# Custom tool
class WebsiteSummarizerTool(BaseTool):
    name: str = "Website Summarizer"
    description: str = "Scrapes a website and returns a detailed summary of its content."
    args_schema: Type[BaseModel] = WebsiteInput

    def _run(self, url: str) -> str:
        def fetch_website_html(target_url):
            try:
                response = requests.get(target_url)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                return f"Error fetching the website: {e}"

        def extract_text(html_content):
            soup = BeautifulSoup(html_content, 'html.parser')
            return ' '.join(soup.stripped_strings)

        if not url:
            return "Invalid URL provided."

        html_content = fetch_website_html(url)
        if not html_content or html_content.startswith("Error"):
            return f"Failed to fetch content from: {url}"

        text = extract_text(html_content)
        chunks = [text[i:i + 8000] for i in range(0, len(text), 8000)]
        summaries = []

        for chunk in chunks:
            try:
                chat_completion = openai.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                "Analyze and make a LONG summary of the content below. "
                                "Make sure to include ALL relevant information. "
                                "Return only the summary.\n\nCONTENT\n----------\n" + chunk
                            ),
                        }
                    ],
                    model="gpt-4o",
                )
                summaries.append(chat_completion.choices[0].message.content)
            except Exception as e:
                summaries.append(f"Error during OpenAI summarization: {e}")

        final_summary = "\n\n".join(summaries)
        return f"Scraped content summary:\n{final_summary}"
