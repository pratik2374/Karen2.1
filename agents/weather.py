from dotenv import load_dotenv
load_dotenv()
import regex as re
from agno.agent import Agent
from agno.models.openai import OpenAIChat

import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENWEATHER_API_KEY"] = os.getenv("WEATHER_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from agno.tools.openweather import OpenWeatherTools

class WeatherAgent:
    def __init__(self):
        
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
        )

    def get_weather_response_from_user_input(self, user_input: str):
            """
            Get weather response for a user input string (e.g., 'What's the weather in Delhi?')
            Prints the response in markdown format.
            """
            response = self.agent.run(user_input)
            return response
    
temp = WeatherAgent()
print(temp.get_weather_response_from_user_input("What's the weather in New Delhi?").content)
print(temp.get_weather_response_from_user_input("Is it raining in London?").content)

