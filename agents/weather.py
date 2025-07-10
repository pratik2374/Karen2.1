from dotenv import load_dotenv
load_dotenv()

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
                OpenWeatherTools(units="metric"),
            ],
            markdown=True,
        )

    def get_weather_response_from_user_input(self, user_input: str):
        """
        Get weather response for a user input string (e.g., 'What's the weather in Delhi?')
        Prints the response in markdown format.
        """
        self.agent.print_response(user_input, markdown=True)

# Example usage
if __name__ == "__main__":   
    weather_agent = WeatherAgent()
    user_input = input("Enter your weather query (e.g., What's the weather in Delhi?): ")
    weather_agent.get_weather_response_from_user_input(user_input)