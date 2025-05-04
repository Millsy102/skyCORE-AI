
import json
from pathlib import Path

class MemoryCore:
    def __init__(self, runtime):
        self.runtime = runtime
        self.path = Path(__file__).resolve().parent.parent / "config" / "memory.json"
        self.data = self.load()

    def load(self):
        if not self.path.exists():
            self.save({"affection": 0, "memory": []})
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data):
        self.data = data
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def update_memory(self, new_entry):
        self.data.get("memory", []).append(new_entry)
        self.save(self.data)
