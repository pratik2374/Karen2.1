from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
from dateutil import parser
from datetime import datetime
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is not None:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

composio_toolset = ComposioToolSet(api_key="8qr3cp4a09u4zfsgd7tuzm")
tools = composio_toolset.get_tools(actions=['GOOGLECALENDAR_CREATE_EVENT', 'GOOGLECALENDAR_FIND_EVENT'])

def extract_date_from_query(query: str) -> datetime:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    system_prompt = """
    If the query mentions a date, extract it and return in 'YYYY-MM-DD' format only.
    If no date is mentioned, just reply with: "NO_DATE"
    Only return a single line output. No explanation.
    """

    response = llm.invoke(f"{system_prompt}\n\nQuery: {query}")
    if isinstance(response.content, list):
        date_str = str(response.content[0]).strip()
    else:
        date_str = str(response.content).strip()

    if date_str == "NO_DATE":
        return datetime.today()  # Correct current system date
    else:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return datetime.today()  # Fallback if parsing fails

def find_event(query: str):
    date_obj = extract_date_from_query(query)

    start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    time_min = start_of_day.strftime('%Y-%m-%dT%H:%M:%S')
    time_max = end_of_day.strftime('%Y-%m-%dT%H:%M:%S')

    calendar_finder_agent = Agent(
        role="Calendar Finder Agent",
        goal="Find relevant events based on time constraints.",
        backstory="You are an assistant designed to retrieve calendar events using composio tools.",
        verbose=True,
        tools=list(tools),
        llm=ChatOpenAI(model="gpt-4o"),
    )

    task = Task(
        description=f"""
        Fetch all calendar events with the following constraints:
        timeMin: {time_min}
        timeMax: {time_max}
        Query context: {query}
        """,
        agent=calendar_finder_agent,
        expected_output="List of all events matching the criteria."
    )

    crew = Crew(agents=[calendar_finder_agent], tasks=[task])
    result = crew.kickoff()
    print(result)
    

def create_event(event):
    # Define agent
    calender_agent = Agent(
        role="Calender Agent",
        goal="""You are an AI agent that is responsible for creating a new event in the calender, 
                if some field are unknown to you make best guess according to the query""",
        backstory=(
            "You are AI agent that is responsible for creating a new event in the calender"
        ),
        verbose=True,
        tools=list(tools),
        llm=ChatOpenAI(model="gpt-4o"),
    )
    task = Task(
        description=f"Create a new event in the calender with the following details within the year 2025: \n{event}",
        agent=calender_agent,
        expected_output="The event created in the calender"
    )
    my_crew = Crew(agents=[calender_agent], tasks=[task])

    result = my_crew.kickoff()
    print(result)

def get_events(query: str):
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
    )

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

    If any field is missing, make a best guess. Output only the Python dictionary, nothing else.
    """

    response = llm.invoke(f"{system_prompt}\n\nQuery: {query}")
    create_event(event=response)

find_event("Get todays events ")
