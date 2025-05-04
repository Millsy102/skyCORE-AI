# 📦 Module imports
import os
import yaml
from pathlib import Path

# Class: PluginUpdater: — defines main behavior for plugin_updater.py
class PluginUpdater:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.plugins = Path("plugins")

# Function: check_for_updates — handles a core step in this module
    def check_for_updates(self):
        updates = {}
        for p in self.plugins.glob("*"):
            manifest = p / "plugin.yaml"
            version_file = p / "version.txt"
            if manifest.exists() and version_file.exists():
                local = yaml.safe_load(manifest.read_text()).get("version", "0.0.1")
                current = version_file.read_text().strip()
                if current != local:
                    updates[p.name] = {"current": current, "manifest": local}
    # 🏁 Returning result
        return updates

updater = PluginUpdater()