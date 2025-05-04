# 📦 Module imports
import importlib.util
import os
import sys
from src.logging_engine import log_trace

# Class: PluginExecutor: — defines main behavior for plugin_executor.py
class PluginExecutor:
# Function: __init__ — handles a core step in this module
    def __init__(self, plugin_root="plugins"):
        self.plugin_root = plugin_root
        self.cache = {}

# Function: run — handles a core step in this module
    def run(self, plugin_name: str, user_input: str) -> str:
        plugin_path = os.path.join(self.plugin_root, plugin_name, "plugin.py")
        if not os.path.exists(plugin_path):
            raise FileNotFoundError(f"Plugin file not found: {plugin_path}")

        plugin = self._load_plugin(plugin_name, plugin_path)
        if not hasattr(plugin, "Plugin"):
            raise AttributeError(f"Plugin '{plugin_name}' is missing a 'Plugin' class.")

        instance = plugin.Plugin()
        if not hasattr(instance, "execute"):
            raise AttributeError(f"Plugin '{plugin_name}' class has no 'execute()' method.")

        try:
            result = instance.execute(user_input)
            log_trace("PluginExecutor", "run", "plugin", f"Executed plugin '{plugin_name}'")
    # 🏁 Returning result
            return result
        except Exception as e:
            log_trace("PluginExecutor", "run", "error", f"Plugin '{plugin_name}' failed: {str(e)}")
    # 🏁 Returning result
            return f"Error running plugin '{plugin_name}': {str(e)}"

# Function: _load_plugin — handles a core step in this module
    def _load_plugin(self, plugin_name, plugin_path):
        if plugin_name in self.cache:
    # 🏁 Returning result
            return self.cache[plugin_name]

        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[plugin_name] = module
        spec.loader.exec_module(module)
        self.cache[plugin_name] = module
        log_trace("PluginExecutor", "_load_plugin", "load", f"Loaded plugin '{plugin_name}'")
    # 🏁 Returning result
        return module
