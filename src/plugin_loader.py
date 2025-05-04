# 📦 Module imports
import os
import yaml
from src.logging_engine import log_trace

# Class: PluginLoader: — defines main behavior for plugin_loader.py
class PluginLoader:
# Function: __init__ — handles a core step in this module
    def __init__(self, plugin_root="plugins"):
        self.plugin_root = plugin_root
        self.plugins = {}
        self._scan()

# Function: _scan — handles a core step in this module
    def _scan(self):
        if not os.path.exists(self.plugin_root):
    # 🏁 Returning result
            return

        for folder in os.listdir(self.plugin_root):
            folder_path = os.path.join(self.plugin_root, folder)
            manifest_path = os.path.join(folder_path, "manifest.yaml")
            if os.path.isdir(folder_path) and os.path.exists(manifest_path):
                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        metadata = yaml.safe_load(f)
                        metadata["path"] = folder_path
                        self.plugins[metadata["name"]] = metadata
                        log_trace("PluginLoader", "_scan", "load", f"Loaded plugin manifest: {metadata['name']}")
                except Exception as e:
                    log_trace("PluginLoader", "_scan", "error", f"Failed to load {folder}: {str(e)}")

# Function: load_all — handles a core step in this module
    def load_all(self):
        self._scan()

# Function: get_all_plugins — handles a core step in this module
    def get_all_plugins(self) -> list:
    # 🏁 Returning result
        return list(self.plugins.values())

# Function: get_plugin_by_command — handles a core step in this module
    def get_plugin_by_command(self, command: str) -> dict:
        for plugin in self.plugins.values():
            if "triggers" in plugin and command in plugin["triggers"]:
    # 🏁 Returning result
                return plugin
    # 🏁 Returning result
        return {}

# Function: get_all_triggers — handles a core step in this module
    def get_all_triggers(self) -> list:
        triggers = []
        for plugin in self.plugins.values():
            triggers.extend(plugin.get("triggers", []))
    # 🏁 Returning result
        return list(set(triggers))

# Function: is_loaded — handles a core step in this module
    def is_loaded(self, plugin_name: str) -> bool:
    # 🏁 Returning result
        return plugin_name in self.plugins

# Function: get_plugin_path — handles a core step in this module
    def get_plugin_path(self, plugin_name: str) -> str:
    # 🏁 Returning result
        return self.plugins.get(plugin_name, {}).get("path", "")
    
# Function: match_plugin_trigger — handles a core step in this module
    def match_plugin_trigger(self, input_text: str) -> dict:
        for plugin in self.plugins.values():
            if any(trigger.lower() in input_text.lower() for trigger in plugin.get("triggers", [])):
    # 🏁 Returning result
                return plugin
    # 🏁 Returning result
        return {}
