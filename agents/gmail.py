from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
import os
from dotenv import load_dotenv


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is not None:
    os.environ['OPENAI_API_KEY'] = openai_api_key
else:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize Composio toolset
composio_toolset = ComposioToolSet(api_key="8qr3cp4a09u4zfsgd7tuzm")
tools = composio_toolset.get_tools(actions=['GMAIL_FETCH_EMAILS','GMAIL_CREATE_EMAIL_DRAFT'])

def fetch_email(no_of_emails: int = 3):
    """
    Fetch the latest email from your inbox and return as response
    """
    # Define agent
    mail_fetching_agent = Agent(
        role="Email Fetching Agent",
        goal="""You are an AI agent that is responsible for fetching the latest email from your inbox and return as response""",
        backstory=(
            "You are an AI agent that is responsible for fetching the latest email from your inbox and return as response"
        ),
        verbose=True,
        tools=list(tools),
        llm=ChatOpenAI(model="gpt-4o")
    )
    task = Task(
        description="Fetch the 3 latest email from your inbox and return as response",
        agent=mail_fetching_agent,
        expected_output="The summary of the latest 3 emails from your inbox"
    )

    # Initialize Crew
    my_crew = Crew(agents=[mail_fetching_agent], tasks=[task])

    result = my_crew.kickoff()
    return str(result)

def create_email_draft(subject: str, body: str, recipient: str, sender: str):
    """
    Create a draft email with the subject and body provided
    """
    mail = f"""
    Recipient: {recipient}\n\n
    Subject: {subject}\n\n
    Body: {body}\n\n
    with regards,\n
    {sender}
    """
    # Define agent
    mail_drafting_agent = Agent(
        role="Email Drafting Agent",
        goal="""You are an AI agent that is responsible for creating a draft email""",
        backstory=(
            "You are an AI agent that is responsible for creating a draft email having the subject, body and recipient provided"
        ),
        verbose=True,
        tools=list(tools),
        llm=ChatOpenAI(model="gpt-4o")
    )
    task = Task(
        description=f"Create a draft email with the subject and body and other details provided below \n\nmail : {mail}",
        agent=mail_drafting_agent,
        expected_output="The draft email with given subject, body and recipient and sender"
    )
    my_crew = Crew(agents=[mail_drafting_agent], tasks=[task])
    result = my_crew.kickoff()
    return str(result)

# print(create_email_draft("Hello", "This is a test email", "pratikgond2005@gmail.com", "Pratik Gond"))