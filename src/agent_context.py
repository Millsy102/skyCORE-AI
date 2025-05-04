# 📦 Module imports
from src.logger import log

# Class: AgentContext: — defines main behavior for agent_context.py
class AgentContext:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.state = {}

# Function: update — handles a core step in this module
    def update(self, agent_id, data):
        self.state[agent_id] = data
        log(f"[AgentContext] Updated context for {agent_id}")

# Function: get — handles a core step in this module
    def get(self, agent_id):
    # 🏁 Returning result
        return self.state.get(agent_id, {})

agent_context = AgentContext()