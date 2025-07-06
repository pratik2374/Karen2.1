# agents/agentmanager.py
import importlib
import os

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.agent_names = [
            'gmail',
            'RAG',
            'search',
            'weather',
            'tinyurl',
            'Gcalendar',
            # Add more here
        ]
        self.load_agents()

    def load_agents(self):
        for name in self.agent_names:
            try:
                module = importlib.import_module(f'agents.{name}')
                if hasattr(module, 'agent'):
                    self.agents[name] = module.agent
                else:
                    print(f"[WARN] {name}.py missing `agent` object")
            except Exception as e:
                print(f"[ERROR] Couldn't load agent '{name}': {e}")

    def get_agent(self, name):
        return self.agents.get(name)

    def run(self, name, method, *args, **kwargs):
        agent = self.get_agent(name)
        if not agent:
            raise ValueError(f"No agent named '{name}' found.")
        if not hasattr(agent, method):
            raise AttributeError(f"'{name}' agent has no method '{method}'")
        return getattr(agent, method)(*args, **kwargs)

    def list_agents(self):
        return list(self.agents.keys())
