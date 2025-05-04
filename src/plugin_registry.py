# 📦 Module imports
from pathlib import Path
import json

REGISTRY_FILE = Path("config/plugin_registry.json")

# Class: PluginRegistry: — defines main behavior for plugin_registry.py
class PluginRegistry:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.state = {}
        self.load()

# Function: load — handles a core step in this module
    def load(self):
        if REGISTRY_FILE.exists():
            self.state = json.loads(REGISTRY_FILE.read_text())
        else:
            self.state = {}
            self.save()

# Function: save — handles a core step in this module
    def save(self):
        REGISTRY_FILE.write_text(json.dumps(self.state, indent=2))

# Function: set_state — handles a core step in this module
    def set_state(self, plugin_name, enabled=True, version="0.0.1"):
        self.state[plugin_name] = {"enabled": enabled, "version": version}
        self.save()

# Function: get_enabled_plugins — handles a core step in this module
    def get_enabled_plugins(self):
    # 🏁 Returning result
        return {k: v for k, v in self.state.items() if v.get("enabled")}

registry = PluginRegistry()