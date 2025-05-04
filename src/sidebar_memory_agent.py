
import json
import os

class SidebarMemoryAgent:
    def __init__(self, memory_file="memory/sidebar_usage.json"):
        self.memory_file = memory_file
        self.usage = {}
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.usage = json.load(f)
            except:
                self.usage = {}

    def increment(self, group):
        self.usage[group] = self.usage.get(group, 0) + 1
        self.save()

    def most_used(self):
        if not self.usage:
            return "🧠 AI Core"
        return max(self.usage, key=self.usage.get)

    def save(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump(self.usage, f, indent=2)
