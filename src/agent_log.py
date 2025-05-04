
import os
import json
import time
from pathlib import Path

class AgentLog:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.console_dir = self.project_path / ".memory"
        self.console_dir.mkdir(exist_ok=True)
        self.current_log = []

    def log_step(self, action_type, description, data=None):
        entry = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": action_type,
            "description": description,
            "data": data or {}
        }
        self.current_log.append(entry)

    def save_log(self, label="task_console"):
        filename = f"console_{label}_{time.strftime('%Y%m%d-%H%M%S')}.json"
        path = self.console_dir / filename
        with open(path, "w") as f:
            json.dump(self.current_log, f, indent=2)
        return str(path)

    def reset_log(self):
        self.current_log = []
