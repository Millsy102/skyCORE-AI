
import os
import json
import time
from pathlib import Path

MEMORY_DIR = ".memory"
SUMMARY_INTERVAL = 5

class MemoryEngine:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.memory_path = self.base_path / MEMORY_DIR
        self.memory_path.mkdir(exist_ok=True)
        self.index_path = self.memory_path / "memory_index.json"
        self.load_index()

    def load_index(self):
        if self.index_path.exists():
            with open(self.index_path, "r") as f:
                self.index = json.load(f)
        else:
            self.index = {"latest": None, "log": []}
            self.save_index()

    def save_index(self):
        with open(self.index_path, "w") as f:
            json.dump(self.index, f, indent=2)

    def record_action(self, name, data):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{len(self.index['log']):03d}_{name}.json"
        filepath = self.memory_path / filename

        with open(filepath, "w") as f:
            json.dump({
                "timestamp": timestamp,
                "name": name,
                "data": data
            }, f, indent=2)

        self.index["log"].append({
            "file": filename,
            "type": "action",
            "timestamp": timestamp
        })

        self.save_index()

        if len([e for e in self.index["log"] if e["type"] == "action"]) % SUMMARY_INTERVAL == 0:
            self.generate_summary()

    def generate_summary(self):
        last_summary_index = max(
            [i for i, e in enumerate(self.index["log"]) if e["type"] == "summary"],
            default=-1
        )
        recent_actions = self.index["log"][last_summary_index+1:]

        summary_data = {
            "summary": f"Summary of {len(recent_actions)} actions.",
            "actions": recent_actions
        }

        filename = f"summary_{len([e for e in self.index['log'] if e['type'] == 'summary'])+1}.json"
        filepath = self.memory_path / filename

        with open(filepath, "w") as f:
            json.dump(summary_data, f, indent=2)

        self.index["log"].append({
            "file": filename,
            "type": "summary",
            "timestamp": time.strftime("%Y%m%d-%H%M%S")
        })

        self.index["latest"] = filename
        self.save_index()

    def get_latest_context(self):
        latest = self.index.get("latest")
        if not latest:
            return ""
        path = self.memory_path / latest
        if path.exists():
            with open(path, "r") as f:
                return f.read()
        return ""
