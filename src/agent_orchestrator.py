
from agent_companion import CompanionAgent

class AgentOrchestrator:
    def __init__(self):
        self.active_agent = None

    def load_agent(self, persona_dict):
        self.active_agent = CompanionAgent(persona_dict)

    def respond(self, message):
        if self.active_agent:
            return self.active_agent.speak(message)
        return "❌ No agent loaded"
