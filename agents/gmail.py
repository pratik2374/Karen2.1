# gmail.py
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet
from dotenv import load_dotenv
import os
import re


class GmailAgent:
    def __init__(self):
        """
        Initialize the GmailAgent by loading environment variables and setting up tools.
        """
        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        composio_key = os.getenv('COMPOSIO_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        
        os.environ['OPENAI_API_KEY'] = openai_api_key
        
        self.composio_toolset = ComposioToolSet(api_key=composio_key)
        self.tools = self.composio_toolset.get_tools(actions=[
            'GMAIL_FETCH_EMAILS', 
            'GMAIL_CREATE_EMAIL_DRAFT',
            'GMAIL_SEND_EMAIL'
        ])

        self.llm = ChatOpenAI(model="gpt-4o")

        self.email_knowledge_base = {
        "pradum": "123103008@nitkkr.ac.in",
        "kush": "123103005@nitkkr.ac.in",
        "saransh": "123103002@nitkkr.ac.in",
        "myself": "pratikgond2005@gmail.com",
        "abhay": "abhaysharma2277@gmail.com"
        }
        
        # Sender information
        self.sender_name = "Karen"
        self.sender_email = "itamazes@gmail" #"karen@assistant.com"
        

    def fetch_email(self, no_of_emails: int = 3) -> str:
        """
        Fetch the latest emails using CrewAI.

        Args:
            no_of_emails (int): Number of emails to fetch. Default is 3.

        Returns:
            str: Summary of fetched emails.
        """
        agent = Agent(
            role="Email Fetching Agent",
            goal="Fetch the latest emails from inbox",
            backstory="An expert email-fetching AI agent.",
            verbose=True,
            tools=self.tools,
            llm=self.llm
        )

        task = Task(
            description=f"Fetch the {no_of_emails} latest emails from the inbox and return as response",
            agent=agent,
            expected_output=f"The summary of the latest {no_of_emails} emails"
        )

        crew = Crew(agents=[agent], tasks=[task])
        return str(crew.kickoff())

    def create_email_draft(self, subject: str, body: str, recipient: str, sender: str) -> str:
        """
        Create an email draft with provided details.

        Args:
            subject (str): Subject of the email.
            body (str): Body of the email.
            recipient (str): Recipient email address.
            sender (str): Sender's name.

        Returns:
            str: Generated email draft.
        """
        mail = f"""
        Recipient: {recipient}\n\n
        Subject: {subject}\n\n
        Body: {body}\n\n
        With regards,\n
        {sender}
        """

        agent = Agent(
            role="Email Drafting Agent",
            goal="Draft professional emails",
            backstory="An expert AI in writing email drafts based on user inputs.",
            verbose=True,
            tools=self.tools,
            llm=self.llm
        )

        task = Task(
            description=f"Create a draft email using the following details:\n\n{mail}",
            agent=agent,
            human_input=True,
            expected_output="A complete email draft with subject, body, recipient, and sender."
        )

        crew = Crew(agents=[agent], tasks=[task])
        return str(crew.kickoff())
        
    # Knowledge base for email mappings
    

    def resolve_recipient(self, recipient_input: str) -> str:
        """
        Resolve recipient from natural language input using knowledge base.
        
        Args:
            recipient_input (str): Natural language recipient description
            
        Returns:
            str: Resolved email address
        """
        recipient_input = recipient_input.lower().strip()
        
        # Direct email address
        if '@' in recipient_input:
            return recipient_input
        
        # Check knowledge base
        for name, email in self.email_knowledge_base.items():
            if name.lower() in recipient_input:
                return email
        
        # If not found, return the input as is (might be a new email)
        return recipient_input

    def process_natural_language_request(self, request: str) -> str:
        """
        Process natural language requests and execute appropriate Gmail operations.
        
        Args:
            request (str): Natural language request
            
        Returns:
            str: Response from the executed operation
        """
        request_lower = request.lower()
        
        # Create main agent for processing requests
        main_agent = Agent(
            role="Gmail Operations Controller",
            goal="Process natural language requests and execute appropriate Gmail operations",
            backstory="""You are an expert Gmail operations controller. You understand natural language 
            requests and can extract necessary information to perform email operations. You have access 
            to a knowledge base of email mappings and can resolve recipients from names to email addresses.""",
            verbose=True,
            tools=self.tools,
            llm=self.llm
        )

        # Determine operation type and create appropriate task
        if any(word in request_lower for word in ['fetch', 'get', 'read', 'check', 'show', 'latest', 'recent']):
            # Fetch emails operation
            task = Task(
                description=f"""Process this request: "{request}"
                
                Knowledge Base:
                - Email mappings: {self.email_knowledge_base}
                - Sender: {self.sender_name} ({self.sender_email})
                
                Extract the number of emails to fetch (default to 3 if not specified) and fetch them.""",
                agent=main_agent,
                expected_output="Summary of the fetched emails with proper formatting"
            )
        elif any(word in request_lower for word in ['draft']):
            task = Task(
                description=f"""Process this request: "{request}"
                
                Knowledge Base:
                - Email mappings: {self.email_knowledge_base}
                - Sender: {self.sender_name} ({self.sender_email})
                
                Extract the following information:
                1. Recipient (resolve using knowledge base if name is provided)
                2. Subject
                3. Body content
                4. Any additional context
                
                Then create an email draft with the extracted information.""",
                agent=main_agent,
                human_input=True,
                expected_output="A complete email draft with all necessary details"
            )
        elif any(word in request_lower for word in ['send', 'write', 'compose', 'create', 'email']):
            # Create email draft operation
            task = Task(
                description=f"""Process this request: "{request}"
                
                Knowledge Base:
                - Email mappings: {self.email_knowledge_base}
                - Sender: {self.sender_name} ({self.sender_email})
                
                Extract the following information:
                1. Recipient (resolve using knowledge base if name is provided)
                2. Subject
                3. Body content
                4. Any additional context
                
                Then create an send email with the extracted information.
                in the end always sign off with :
                Yours Karen
                (Best assistant 😉)
                """,
                agent=main_agent,
                human_input=True,
                expected_output="A complete email draft with all necessary details"
            )
        else:
            # General processing
            task = Task(
                description=f"""Process this request: "{request}"
                
                Knowledge Base:
                - Email mappings: {self.email_knowledge_base}
                - Sender: {self.sender_name} ({self.sender_email})
                
                Determine what Gmail operation is needed and execute it appropriately.""",
                agent=main_agent,
                expected_output="Appropriate response based on the request"
            )

        crew = Crew(agents=[main_agent], tasks=[task])
        return str(crew.kickoff())

    def add_email_mapping(self, name: str, email: str):
        """
        Add a new email mapping to the knowledge base.
        
        Args:
            name (str): Person's name
            email (str): Email address
        """
        self.email_knowledge_base[name.lower()] = email.lower()

    def get_email_mappings(self) -> dict:
        """
        Get all email mappings from the knowledge base.
        
        Returns:
            dict: All email mappings
        """
        return self.email_knowledge_base.copy()

    def update_sender_info(self, name: str, email: str):
        """
        Update sender information.
        
        Args:
            name (str): Sender's name
            email (str): Sender's email
        """
        self.sender_name = name
        self.sender_email = email

    def get_method(self):
        available_methods = {
            "process_natural_language_request": """can create a draft, send to user himself, friends
            , has inbuilt contacts database, also it can fetch n numbers of mail from user 
            inbox, to use this mail agent just call mail_agent.process_natural_language_request(query), pass query in function"""
        }
        return available_methods



