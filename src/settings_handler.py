# 📦 Module imports
import json
import os
from src.logging_engine import log_trace

# Class: SettingsHandler: — defines main behavior for settings_handler.py
class SettingsHandler:
# Function: __init__ — handles a core step in this module
    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path
        self.settings = {}
        self._load()

# Function: _load — handles a core step in this module
    def _load(self):
        if not os.path.exists(self.config_path):
            self.settings = {}
    # 🏁 Returning result
            return
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.settings = json.load(f)
        log_trace("SettingsHandler", "_load", "init", "Settings loaded")

# Function: get — handles a core step in this module
    def get(self, key: str, default=None):
    # 🏁 Returning result
        return self.settings.get(key, default)

# Function: set — handles a core step in this module
    def set(self, key: str, value):
        self.settings[key] = value
        log_trace("SettingsHandler", "set", "config", f"{key} updated")
        self._save()

# Function: delete — handles a core step in this module
    def delete(self, key: str):
        if key in self.settings:
            del self.settings[key]
            log_trace("SettingsHandler", "delete", "config", f"{key} removed")
            self._save()

# Function: _save — handles a core step in this module
    def _save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)

# Function: dump — handles a core step in this module
    def dump(self):
    # 🏁 Returning result
        return self.settings.copy()
