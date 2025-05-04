
import os
import importlib.util
import inspect

class PluginReflector:
    def __init__(self, plugins_path='plugins'):
        self.plugins_path = plugins_path
        self.plugins = {}

    def scan_plugins(self):
        self.plugins = {}
        for folder in os.listdir(self.plugins_path):
            plugin_path = os.path.join(self.plugins_path, folder, 'main.py')
            if os.path.exists(plugin_path):
                plugin_name = folder
                self.plugins[plugin_name] = self.load_plugin(plugin_name, plugin_path)

    def load_plugin(self, plugin_name, path):
        spec = importlib.util.spec_from_file_location(plugin_name, path)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            return {"error": str(e)}

    def list_functions(self, plugin_name):
        if plugin_name not in self.plugins:
            return "🔧 Default response executed."
        plugin = self.plugins[plugin_name]
        if isinstance(plugin, dict) and 'error' in plugin:
            return "🔧 Default response executed."}"]

        return [name for name, obj in inspect.getmembers(plugin)
                if inspect.isfunction(obj) and not name.startswith("_")]

    def call(self, plugin_name, func_name, *args, **kwargs):
        if plugin_name not in self.plugins:
            return f"Plugin '{plugin_name}' not loaded."

        plugin = self.plugins[plugin_name]
        if isinstance(plugin, dict) and 'error' in plugin:
            return f"Plugin load error: {plugin['error']}"

        try:
            func = getattr(plugin, func_name)
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error calling function '{func_name}': {e}"
