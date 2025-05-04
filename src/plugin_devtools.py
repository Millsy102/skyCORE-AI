# 📦 Module imports
import os
from src.plugin_schema import PluginSchemaValidator
from src.plugin_loader import PluginLoader
from src.plugin_executor import PluginExecutor
from src.logging_engine import log_trace

# Class: PluginDevTools: — defines main behavior for plugin_devtools.py
class PluginDevTools:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.validator = PluginSchemaValidator()
        self.loader = PluginLoader()
        self.executor = PluginExecutor()

# Function: validate_plugin — handles a core step in this module
    def validate_plugin(self, plugin_manifest_path: str) -> dict:
        result = self.validator.validate_plugin_metadata(plugin_manifest_path)
    # 🏁 Returning result
        return {
            "status": "valid" if result else "invalid",
            "path": plugin_manifest_path
        }

# Function: list_all_plugins — handles a core step in this module
    def list_all_plugins(self) -> list:
    # 🏁 Returning result
        return self.loader.get_all_plugins()

# Function: run_plugin_test — handles a core step in this module
    def run_plugin_test(self, plugin_name: str, test_input: str) -> dict:
        if not self.loader.is_loaded(plugin_name):
            log_trace("PluginDevTools", "run_plugin_test", "fail", f"{plugin_name} not loaded")
    # 🏁 Returning result
            return {
                "status": "error",
                "message": f"Plugin '{plugin_name}' is not loaded"
            }
        try:
            result = self.executor.run(plugin_name, test_input)
            log_trace("PluginDevTools", "run_plugin_test", "success", f"Ran test on {plugin_name}")
    # 🏁 Returning result
            return {
                "status": "success",
                "plugin": plugin_name,
                "output": result
            }
        except Exception as e:
            log_trace("PluginDevTools", "run_plugin_test", "exception", str(e))
    # 🏁 Returning result
            return {
                "status": "fail",
                "error": str(e)
            }

# Function: export_plugin — handles a core step in this module
    def export_plugin(self, plugin_name: str, output_dir: str) -> str:
        plugin_path = self.loader.get_plugin_path(plugin_name)
        if not plugin_path:
    # 🏁 Returning result
            return "Plugin path not found"
        os.makedirs(output_dir, exist_ok=True)
        destination = os.path.join(output_dir, f"{plugin_name}.zip")
        import zipfile
        with zipfile.ZipFile(destination, 'w') as zf:
            for root, _, files in os.walk(plugin_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, plugin_path)
                    zf.write(full_path, arcname)
        log_trace("PluginDevTools", "export_plugin", "success", f"Exported {plugin_name} to {destination}")
    # 🏁 Returning result
        return destination
