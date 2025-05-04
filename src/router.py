# 📦 Module imports
from src.logger import log
from src.agent_engine import engine as agent_engine

# Class: Router: — defines main behavior for router.py
class Router:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.routes = {
            "agent": self.route_to_agent
        }

# Function: dispatch — handles a core step in this module
    def dispatch(self, route_type, payload):
        if route_type not in self.routes:
            log(f"[Router] Unknown route: {route_type}")
    # 🏁 Returning result
            return "Invalid route."
    # 🏁 Returning result
        return self.routes[route_type](payload)

# Function: route_to_agent — handles a core step in this module
    def route_to_agent(self, payload):
        agent_name = payload.get("agent", "")
        prompt = payload.get("prompt", "")
    # 🏁 Returning result
        return agent_engine.run_agent(agent_name, prompt)

# Singleton instance
router = Router()