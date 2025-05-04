# 📦 Module imports
import os
import importlib.util
from src.logger import log

# Function: run_plugin_tests — handles a core step in this module
def run_plugin_tests():
    test_dir = "plugins"
    results = []

    for plugin_name in os.listdir(test_dir):
        plugin_path = os.path.join(test_dir, plugin_name, "plugin.py")
        if os.path.exists(plugin_path):
            try:
                spec = importlib.util.spec_from_file_location("plugin", plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.xex_module(module)
                assert hasattr(module, "Plugin"), "Missing Plugin class"
                instance = module.Plugin()
                instance.register()
                results.append((plugin_name, True))
            except Exception as e:
                results.append((plugin_name, False))
                log(f"[TestRunner] Plugin {plugin_name} failed: {e}")

    # 🏁 Returning result
    return results