from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
from dateutil import parser
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv


class CalendarManager:
    """
    A comprehensive calendar management class that handles event creation,
    finding, and extraction using CrewAI and Composio tools.
    """
    
    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize the CalendarManager with API keys and tools.
        
        Args:
            composio_api_key (str): API key for Composio toolset
            model (str): OpenAI model to use
        """
        self._setup_environment()
        composio_api_key = os.getenv('COMPOSIO_KEY')
        self.model = model
        self.composio_toolset = ComposioToolSet(api_key=composio_api_key)
        self.tools = self.composio_toolset.get_tools(
            actions=['GOOGLECALENDAR_CREATE_EVENT', 'GOOGLECALENDAR_FIND_EVENT']
        )
        self.llm = ChatOpenAI(model=self.model, temperature=0)
    
    def _setup_environment(self):
        """Load environment variables and set up OpenAI API key."""
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key is not None:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        else:
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")
    
    def extract_date_from_query(self, query: str) -> datetime:
        """
        Extract date from natural language query.
        
        Args:
            query (str): Natural language query containing date information
            
        Returns:
            datetime: Extracted date or today's date if no date found
        """
        from datetime import datetime
        from zoneinfo import ZoneInfo  # Built-in from Python 3.9+

        current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
        system_prompt = f"""
        todays date : {current_time}
        If the query mentions a date, extract it and return in 'YYYY-MM-DD' format only.
        If no date is mentioned, just reply with: "NO_DATE"
        Only return a single line output. No explanation.
        """

        response = self.llm.invoke(f"{system_prompt}\n\nQuery: {query}")
        if isinstance(response.content, list):
            date_str = str(response.content[0]).strip()
        else:
            date_str = str(response.content).strip()

        if date_str == "NO_DATE":
            return datetime.today()
        else:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return datetime.today()
    
    def find_events(self, query: str) -> str:
        """
        Find calendar events based on query and date constraints.
        
        Args:
            query (str): Natural language query to find events
            
        Returns:
            str: Result from the crew execution
        """
        date_obj = self.extract_date_from_query(query)

        start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        time_min = start_of_day.strftime('%Y-%m-%dT%H:%M:%S')
        time_max = end_of_day.strftime('%Y-%m-%dT%H:%M:%S')

        calendar_finder_agent = Agent(
            role="Calendar Finder Agent",
            goal="Find relevant events based on time constraints.",
            backstory="You are an assistant designed to retrieve calendar events using composio tools.",
            verbose=True,
            tools=list(self.tools),
            llm=ChatOpenAI(model=self.model),
        )

        task = Task(
            description=f"""
            Fetch all calendar events with the following constraints:
            timeMin: {time_min}
            timeMax: {time_max}
            All time shown in IST time
            Query context: {query}
            """,
            agent=calendar_finder_agent,
            expected_output="List of all events matching the criteria."
        )

        crew = Crew(agents=[calendar_finder_agent], tasks=[task])
        result = crew.kickoff()
        print(result)
        return result
    
    def create_event(self, event_details: str) -> str:
        """
        Create a new calendar event using the provided details.
        
        Args:
            event_details (str): Event details or structured event data
            
        Returns:
            str: Result from the crew execution
        """
        calendar_agent = Agent(
            role="Calendar Agent",
            goal="""You are an AI agent that is responsible for creating a new event in the calendar, 
                    if some fields are unknown to you make best guess according to the query""",
            backstory="You are AI agent that is responsible for creating a new event in the calendar",
            verbose=True,
            tools=list(self.tools),
            llm=ChatOpenAI(model=self.model),
        )
        
        task = Task(
            description=f"Create a new event in the calendar with the following details within the year 2025, and IST timezone: \n{event_details}",
            agent=calendar_agent,
            expected_output="The event created in the calendar"
        )
        
        crew = Crew(agents=[calendar_agent], tasks=[task])
        result = crew.kickoff()
        print(result)
        return result
    
    def extract_event_info(self, query: str) -> dict:
        """
        Extract structured event information from natural language.
        
        Args:
            query (str): Natural language description of the event
            
        Returns:
            dict: Structured event information
        """
        from datetime import datetime
        from zoneinfo import ZoneInfo  # Built-in from Python 3.9+

        current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
        print("Time in India:", current_time.strftime('%Y-%m-%d %H:%M:%S'))
        system_prompt = """
        You are an intelligent assistant that extracts event information from natural language.
        Extract and return the result as a Python dictionary with the following fields:
        - title: Short title of the event
        - description: A brief description
        - start_date: Start date and time in the format YYYY-MM-DDTHH:MM:SS
        - event_duration_hours: Integer
        - event_duration_minutes: Integer
        - location: Physical or virtual meeting location
        - reminders: Always include {"useDefault": true}
        - summary: Same as title

        **NOTE** KEEP TIME IN Always return the time in Indian Standard Time (IST), using a 12-hour format with AM/PM, given query time is based on IST

        If any field is missing, make a best guess. Output only the Python dictionary, nothing else.

        EXAMPLES:(just for example never use this as it is)

        Query: "Schedule a team meeting tomorrow at 2 PM for 1 hour in conference room A"
        {
            "title": "Team Meeting",
            "description": "Team meeting in conference room A",
            "start_date": "2025-06-29T14:00:00",
            "event_duration_hours": 1,
            "event_duration_minutes": 0,
            "location": "Conference Room A",
            "reminders": {"useDefault": true},
            "summary": "Team Meeting"
        }

        Query: "Call with client John about project review on Friday 3 PM for 30 minutes"
        {
            "title": "Client Call - John",
            "description": "Project review call with client John",
            "start_date": "2025-07-04T15:00:00",
            "event_duration_hours": 0,
            "event_duration_minutes": 30,
            "location": "Virtual Meeting",
            "reminders": {"useDefault": true},
            "summary": "Client Call - John"
        }

        Query: "Birthday party at Sarah's house Saturday 7 PM"
        {
            "title": "Birthday Party",
            "description": "Birthday celebration at Sarah's house",
            "start_date": "2025-06-28T19:00:00",
            "event_duration_hours": 3,
            "event_duration_minutes": 0,
            "location": "Sarah's House",
            "reminders": {"useDefault": true},
            "summary": "Birthday Party"
        }

        Query: "Gym workout session Tuesday morning"
        {
            "title": "Gym Workout",
            "description": "Personal workout session at the gym",
            "start_date": "2025-07-01T09:00:00",
            "event_duration_hours": 1,
            "event_duration_minutes": 30,
            "location": "Gym",
            "reminders": {"useDefault": true},
            "summary": "Gym Workout"
        }
        """

        response = self.llm.invoke(f"{system_prompt}\n\nQuery: {query} and current time is {current_time}")
        return response
    
    def create_event_from_query(self, query: str) -> str:
        """
        Create an event by first extracting information from natural language query.
        
        Args:
            query (str): Natural language description of the event to create
            
        Returns:
            str: Result from event creation
        """
        event_info = self.extract_event_info(query)
        return self.create_event(event_details=event_info)
    
    def get_today_events(self) -> str:
        """
        Convenience method to get today's events.
        
        Returns:
            str: Today's events
        """
        return self.find_events("Get today's events")
    
    def get_events_for_date(self, date_str: str) -> str:
        """
        Get events for a specific date.
        
        Args:
            date_str (str): Date in natural language (e.g., "tomorrow", "2025-01-15")
            
        Returns:
            str: Events for the specified date
        """
        return self.find_events(f"Get events for {date_str}")

    def get_method(self):
        available_methods = {
            "get_events_for_date" : "fetches event for specific dates",
            "create_event_from_query" : "creates a event for specific date"
        }


gcalender_agent = CalendarManager()

# agent.create_event_from_query("Schedule a team meeting tomorrow at 3 PM for 1 hour")
# agent.get_events_for_date("Get tommorows all events")
# # Usage example
# if __name__ == "__main__":
#     # Initialize the calendar manager
#     calendar_manager = CalendarManager()
    
#     # Find today's events
#     calendar_manager.get_today_events()
    
#     # Create an event from natural language
#     # calendar_manager.create_event_from_query("Schedule a team meeting tomorrow at 2 PM for 1 hour")
    
#     # Find events for a specific date
#     # calendar_manager.get_events_for_date("tomorrow")