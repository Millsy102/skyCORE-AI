# 📦 Module imports
import os
import importlib.util
import traceback
from core.settings_core import load_settings

# Function: load_plugins — handles a core step in this module
def load_plugins():
    settings = load_settings()
    plugin_dir = "plugins"
    for plugin_name in os.listdir(plugin_dir):
        path = os.path.join(plugin_dir, plugin_name)
        if not os.path.isdir(path) or plugin_name.startswith(".") or "temp" in plugin_name:
            continue

        plugin_main = os.path.join(path, f"{plugin_name}.py")
        if os.path.exists(plugin_main):
            try:
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_main)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception as e:
                traceback.print_exc()
