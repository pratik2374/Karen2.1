from crewai import Agent, Task, Crew, CrewOutput
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
from typing import Dict, Any, List, Union
from dotenv import load_dotenv
from langchain.tools import tool
load_dotenv()
import os

class WeatherAgent:
    def __init__(self):
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        os.environ['OPENAI_API_KEY'] = openai_api_key
        
        composio_key = os.getenv('COMPOSIO_KEY')
        if composio_key is None:
            raise ValueError("COMPOSIO_KEY environment variable is not set")
        
        self.composio_toolset = ComposioToolSet(api_key=composio_key)
        self.weather_tools = list(self.composio_toolset.get_tools(actions=['WEATHERMAP_WEATHER']))
        self.llm = ChatOpenAI()
        # Define the weather agent
        self.weather_agent = Agent(
            role="Weather Information Agent",
            goal="""You are an AI agent that retrieves and summarizes weather information for any given location. 
                    You should extract and format the weather data in a clear, structured manner.
                    IMPORTANT: Convert all temperature values from Kelvin to Celsius using the formula: Celsius = Kelvin - 273.15""",
            backstory=(
                "You are a specialized AI agent with expertise in weather data analysis. "
                "You have access to weather tools and can provide detailed weather information "
                "for any location in the world. You always format your responses clearly and concisely. "
                "You always convert temperatures from Kelvin to Celsius for better readability."
            ),
            verbose=True,
            tools=self.weather_tools,
            llm=self.llm,
        )
    def celsius_cal(self, temp: float) -> float:
        """
        Convert temperature from Kelvin to Celsius
        
        Args:
            temp (float): Temperature in Kelvin
            
        Returns:
            float: Temperature in Celsius
        """
        return temp - 273.15
    
    def get_weather_summary(self, location: str) -> Union[Dict[str, Any], CrewOutput]:
        """
        Get weather summary for a specific location
        
        Args:
            location (str): The location to get weather for (e.g., "New York", "London", "Tokyo")
            
        Returns:
            Dict[str, Any]: Weather data in the specified format
        """
        # Create task for weather retrieval
        weather_task = Task(
            description=f"""Get the current weather information for {location}. 
                          Extract and return the following weather parameters in a structured format:
                          - feels_like: temperature that it feels like (convert from Kelvin to Celsius)
                          - grnd_level: ground level pressure
                          - humidity: humidity percentage
                          - pressure: atmospheric pressure
                          - sea_level: sea level pressure
                          - temp: current temperature (convert from Kelvin to Celsius)
                          - temp_max: maximum temperature (convert from Kelvin to Celsius)
                          - temp_min: minimum temperature (convert from Kelvin to Celsius)
                          
                          IMPORTANT: All temperature values (feels_like, temp, temp_max, temp_min) must be converted from Kelvin to Celsius using the formula: Celsius = Kelvin - 273.15
                          
                          Format the output as a clean dictionary with these exact keys and temperatures in Celsius.""",
            agent=self.weather_agent,
            expected_output="A dictionary containing weather parameters with temperatures in Celsius: feels_like, grnd_level, humidity, pressure, sea_level, temp, temp_max, temp_min"
        )
        
        # Create crew and execute
        weather_crew = Crew(
            agents=[self.weather_agent], 
            tasks=[weather_task]
        )
        
        try:
            result = weather_crew.kickoff()
            print(f"Weather data for {location}:")
            print(result)
            return result
        except Exception as e:
            print(f"Error getting weather data for {location}: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    # Create weather agent instance
    weather_agent = WeatherAgent()
    
    # Get weather for a location
    location = "Howrah"  # You can change this to any location
    weather_data = weather_agent.get_weather_summary(location)