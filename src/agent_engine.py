# 📦 Module imports
from src.logger import log
from src.plugin_loader import load_plugins

# Class: AgentEngine: — defines main behavior for agent_engine.py
class AgentEngine:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.agents = {}

# Function: register_agent — handles a core step in this module
    def register_agent(self, name, handler):
        self.agents[name] = handler
        log(f"[AgentEngine] Registered agent: {name}")

# Function: run_agent — handles a core step in this module
    def run_agent(self, name, prompt):
        if name not in self.agents:
            log(f"[AgentEngine] Unknown agent: {name}")
    # 🏁 Returning result
            return "Agent not found."
        try:
    # 🏁 Returning result
            return self.agents[name](prompt)
        except Exception as e:
            log(f"[AgentEngine] Error in {name}: {e}")
    # 🏁 Returning result
            return str(e)

# removed comment
engine = AgentEngine()

# Function: initialize_agents — handles a core step in this module
def initialize_agents():
    load_plugins()
    log("[AgentEngine] Agents initialized.")