# 📦 Module imports
from src.plugin_loader import PluginLoader
from src.plugin_executor import PluginExecutor
from src.settings_handler import SettingsHandler
from src.logging_engine import log_trace
from src.ethical_guard import EthicalGuard

# Class: CommandRouter: — defines main behavior for command_router.py
class CommandRouter:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.loader = PluginLoader()
        self.executor = PluginExecutor()
        self.settings = SettingsHandler()
        self.guard = EthicalGuard()

# Function: route — handles a core step in this module
    def route(self, user_input: str) -> dict:
        command = self._extract_command(user_input)
        if not command:
    # 🏁 Returning result
            return {
                "text": "Unrecognized command.",
                "plugin": None,
                "status": "error"
            }

        plugin_info = self.loader.get_plugin_by_command(command)
        if not plugin_info:
    # 🏁 Returning result
            return {
                "text": f"No plugin registered for command: {command}",
                "plugin": None,
                "status": "unavailable"
            }

        plugin_name = plugin_info['name']
        if self.guard.block_plugin(plugin_name):
    # 🏁 Returning result
            return {
                "text": f"Execution of '{plugin_name}' is restricted by policy.",
                "plugin": plugin_name,
                "status": "blocked"
            }

        if plugin_info.get("requires_confirmation", True):
    # 🏁 Returning result
            return {
                "text": f"Do you want to run the plugin '{plugin_name}'?",
                "plugin": plugin_name,
                "status": "awaiting_confirmation"
            }

        result = self.executor.run(plugin_name, user_input)
        log_trace("CommandRouter", "route", "plugin", f"Ran plugin: {plugin_name}")

    # 🏁 Returning result
        return {
            "text": result,
            "plugin": plugin_name,
            "status": "executed"
        }

# Function: _extract_command — handles a core step in this module
    def _extract_command(self, user_input: str) -> str:
        if user_input.startswith("/"):
    # 🏁 Returning result
            return user_input.split(" ")[0][1:]
        words = user_input.lower().split()
        for trigger in self.loader.get_all_triggers():
            if trigger.lower() in words:
    # 🏁 Returning result
                return trigger
    # 🏁 Returning result
        return ""
