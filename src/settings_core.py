
import json
from pathlib import Path

class SettingsCore:
    def __init__(self, runtime):
        self.runtime = runtime
        self.path = Path(__file__).resolve().parent.parent / "config" / "settings.json"
        self.defaults = {
            "theme": "dark",
            "api_key": "",
            "first_launch": True,
            "allow_plugin_installs": True
        }
        self.data = self.load()

    def load(self):
        if not self.path.exists():
            self.save(self.defaults)
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, config):
        with open(self.path, "w") as f:
            json.dump(config, f, indent=2)

    def get(self, key, fallback=None):
        return self.data.get(key, fallback)

    def set(self, key, value):
        self.data[key] = value
        self.save(self.data)
