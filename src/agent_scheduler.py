# 📦 Module imports
import threading
import time
from src.logger import log

# Class: AgentScheduler: — defines main behavior for agent_scheduler.py
class AgentScheduler:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.tasks = []
        self.running = False

# Function: schedule — handles a core step in this module
    def schedule(self, agent_func, interval=30):
# Function: runner — handles a core step in this module
        def runner():
            while self.running:
                log("[Scheduler] Triggering agent task...")
                try:
                    agent_func()
                except Exception as e:
                    log(f"[Scheduler] Agent task failed: {e}")
                time.sleep(interval)
        self.running = True
        threading.Thread(target=runner, daemon=True).start()

# Function: stop — handles a core step in this module
    def stop(self):
        self.running = False

scheduler = AgentScheduler()