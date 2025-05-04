# 📦 Module imports
import json
import os
from datetime import datetime

# Class: MemoryAgent: — defines main behavior for memory_agent.py
class MemoryAgent:
# Function: __init__ — handles a core step in this module
    def __init__(self, memory_path="config/memory.json"):
        self.memory_path = memory_path
        self.memory = []
        self.load()

# Function: log — handles a core step in this module
    def log(self, kind, data):
        entry = {
            "time": datetime.utcnow().isoformat(),
            "type": kind,
            "data": data
        }
        self.memory.append(entry)
        self.save()

# Function: save — handles a core step in this module
    def save(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.memory, f, indent=2)

# Function: load — handles a core step in this module
    def load(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r") as f:
                self.memory = json.load(f)

# Function: summarize — handles a core step in this module
    def summarize(self, count=5):
    # 🏁 Returning result
        return self.memory[-count:] if len(self.memory) > count else self.memory