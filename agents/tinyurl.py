from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
composio_toolset = ComposioToolSet(api_key="8qr3cp4a09u4zfsgd7tuzm")
tools = composio_toolset.get_tools(actions=['TINYURL_CREATE_SHORT_URL'])

# Define agent
crewai_agent = Agent(
    role="Sample Agent",
    goal="""You are an AI agent that is responsible for taking actions based on the tools you have""",
    backstory=(
        "You are AI agent that is responsible for taking actions based on the tools you have"
    ),
    verbose=True,
    tools=tools,
    llm=ChatOpenAI(),
)
task = Task(
    description="your task description here",
    agent=crewai_agent,
    expected_output=""
)
my_crew = Crew(agents=[crewai_agent], tasks=[task])

result = my_crew.kickoff()
print(result)

# Alias and URL