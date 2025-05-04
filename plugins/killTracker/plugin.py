import subprocess
import os

class Plugin:
    def __init__(self):
        self.name = "Kill Tracker UI"
        self.triggers = ["launch killtracker", "open kill ui", "run kill tracker"]

    def execute(self, input_data):
        try:
            entry = os.path.join(os.path.dirname(__file__), "sctool_ui", "Kill_main.py")
            subprocess.Popen(["python", entry])
            return {"response": "✅ SCTool Kill Tracker launched."}
        except Exception as e:
            return {"error": str(e)}
