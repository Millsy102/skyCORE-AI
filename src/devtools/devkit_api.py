# 📦 Module imports
from src.plugin_loader import load_plugin
from src.skycore_linter import skycore_linter
from src.plugin_sandbox import sandbox

# Class: DevKitAPI: — defines main behavior for devkit_api.py
class DevKitAPI:
# Function: lint_plugin_code — handles a core step in this module
    def lint_plugin_code(self, code):
    # 🏁 Returning result
        return skycore_linter.lint(code)

# Function: run_plugin_code — handles a core step in this module
    def run_plugin_code(self, code):
    # 🏁 Returning result
        return sandbox.safe_xex(code)

# Function: reload_plugins — handles a core step in this module
    def reload_plugins(self):
    # 🏁 Returning result
        return load_plugin("plugins/")
devkit = DevKitAPI()