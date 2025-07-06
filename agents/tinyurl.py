import tkinter as tk
from tkinter import messagebox
import winsound  # For Windows sound
import pyperclip  # To copy to clipboard
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet
from dotenv import load_dotenv
import os

class basic_utility_agent:
    def __init__(self, model: str = "gpt-4o"):
        self._setup_environment()
        composio_api_key = os.getenv('COMPOSIO_KEY')
        if composio_api_key is None:
            raise EnvironmentError("COMPOSIO_KEY environment variable is not set.")

        self.model = model
        self.composio_toolset = ComposioToolSet(api_key=composio_api_key)
        self.tools = self.composio_toolset.get_tools(actions=['TINYURL_CREATE_SHORT_URL'])
        self.llm = ChatOpenAI(model=self.model, temperature=0)

        self.agent = Agent(
            role="Solve the simple query of user",
            goal="You are an AI agent that can solve the simple query of user using tools",
            backstory="You are responsible for solving user queries and providing valid responses.",
            verbose=True,
            tools=list(self.tools),
            llm=self.llm,
        )

    def _setup_environment(self):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key is not None:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        else:
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set.") 

    def _shorten_link(self, query: str) -> str:
        task = Task(
            description=f"Extract and shorten the link using TinyURL tool: {query}",
            agent=self.agent,
            expected_output="just a link shortened by tinyurl"
        )
        crew = Crew(agents=[self.agent], tasks=[task])
        result = crew.kickoff()
        return result

    def tinyurl(self):
        """Launch GUI to take link, process on Enter, copy result to clipboard, show popup and sound."""

        def on_enter(event=None):
            nonlocal link
            link = entry.get()
            root.destroy()  # Close the entry window

        # Step 1: GUI for link input
        root = tk.Tk()
        root.title("Enter link to shorten")
        root.geometry("500x150")

        root.lift()
        root.attributes('-topmost', True)
        root.after(100, lambda: root.attributes('-topmost', False))  # Allow others to take focus after initial raise


        entry = tk.Entry(root, width=60)
        entry.pack(pady=20)
        entry.bind("<Return>", on_enter)
        entry.focus()

        tk.Label(root, text="Press Enter after typing your link", fg="gray").pack()

        link = None
        root.mainloop()  # Wait until Enter is pressed and window is destroyed

        # Step 2: Process link
        if link:
            try:
                result = self._shorten_link(link)
                # Step 3: Copy to clipboard
                pyperclip.copy(result)
                # Step 4: Show popup and play sound
                self._notify_user("Link copied to clipboard!", result)
            except Exception as e:
                self._notify_user("Error", str(e))

    def _notify_user(self, title, message):
    # Play a sound (Windows default sound)
        try:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except:
            pass

        # Create custom popup window
        popup = tk.Tk()
        popup.title(title)
        popup.geometry("300x100")
        popup.attributes('-topmost', True)
        popup.after(1000, popup.destroy)  # Destroy after 1 second

        label = tk.Label(popup, text=message, font=("Helvetica", 12), fg="green")
        label.pack(expand=True)

        popup.mainloop()


example = basic_utility_agent();
example.tinyurl()
