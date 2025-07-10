from dotenv import load_dotenv
load_dotenv()
import regex as re
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.openweather import OpenWeatherTools
import os

class WeatherAgent:
    def __init__(self, composio_key: str = None):
        """
        composio_key: (str) Composio API key. If not provided, will use the COMPOSIO_KEY environment variable.
        Example usage:
            weather_agent = WeatherAgent()
        """
        if composio_key is None:
            composio_key = os.getenv("COMPOSIO_KEY")
        if not composio_key:
            raise ValueError("Composio key must be provided either as an argument or in the COMPOSIO_KEY environment variable.")
        
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[
                OpenWeatherTools(
                    units="metric",
                    current_weather=True,
                    forecast=True,
                    air_pollution=True,
                    geocoding=True
                ),
            ],
            description="""
                You are Karen Weather, an intelligent weather agent.

                🔹 **Your role:** Provide accurate, real-time weather information to users.

                🔹 **How to respond:**
                - **Always use the weather tool** to answer weather-related questions (e.g., temperature, humidity, sunrise, sunset, UV index, air quality, forecasts). Never guess or generate data yourself.
                - For non-weather queries, respond politely that you are a weather assistant and cannot answer unrelated questions.

                🔹 **Examples:**

                User: "What's the temperature in New Delhi?"
                Assistant: *Call the weather tool with 'New Delhi' as input and return the result.*

                User: "Is it raining in London?"
                Assistant: *Call the weather tool with 'London' as input and return the result.*

                User: "Tell me the capital of France."
                Assistant: "I am a weather assistant and can only provide weather information. Please ask a weather-related question."

                User: "Will it be sunny in Bangalore tomorrow?"
                Assistant: *Call the weather tool with 'Bangalore' as input and provide forecast details if available.*

                🔹 **Important:**
                - Never fabricate weather data.
                - Always prefer tool usage for any weather-related question.
                - Keep responses concise, clear, and structured with units and location context.

                Thank you.
            """,
            markdown=True,
        )

    def get_weather_response_from_user_input(self, user_input: str):
            """
            Get weather response for a user input string (e.g., 'What's the weather in Delhi?')
            Prints the response in markdown format.
            """
            response = self.agent.print_response(user_input, markdown=True)
            self.response = response
            return response

