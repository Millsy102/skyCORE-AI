from src.plugin_loader import PluginLoader
from src.command_parser import CommandParser
from src.auto_install_handler import AutoInstallHandler
from src.plugin_suggestion_engine import PluginSuggestionEngine
from src.ai_automation_layer import AIAutomationLayer

class PluginResponder:
    def __init__(self, runtime=None):
        self.loader = PluginLoader()
        self.parser = CommandParser()
        self.installer = AutoInstallHandler()
        self.suggester = PluginSuggestionEngine()
        self.runtime = runtime

    def handle(self, user_input: str):
        intent = self.parser.parse(user_input)
        action = intent.get("action")

        if action == "plugin":
            plugin_name = intent["name"].strip().split()[0].lower() + "".join(w.capitalize() for w in intent["name"].strip().split()[1:])
            if plugin_name in self.loader.plugins:
                return self.loader.plugins[plugin_name].execute({"input": user_input})

            # Attempt auto-install from GitHub ZIP (SkyCore default)
            guess_url = f"https://github.com/skycore-ai/{plugin_name}/archive/refs/heads/main.zip"
            install_status = self.installer.install_from_github_zip(guess_url, plugin_name)
            registration = self.installer.try_register_plugin(self.runtime, plugin_name)

            self.loader = PluginLoader()
            if plugin_name in self.loader.plugins:
                return {
                    "install": install_status,
                    "register": registration,
                    "run": self.loader.plugins[plugin_name].execute({"input": user_input})
                }

            # Search suggestions if not found
            suggestions = self.suggester.search_github_plugins(plugin_name)
            return {
                "error": f"Plugin '{plugin_name}' not found or install failed.",
                "suggestions": suggestions
            }

        elif action == "profile":
            traits = ["default", "intelligent"]
            notes = "User-defined profile"
            return AIAutomationLayer().generate_profile(intent["name"], traits, notes)

        elif action == "config":
            settings = {"debug": True}
            return AIAutomationLayer().generate_config(intent["name"], settings)

        return {"note": "No plugin routed, fallback to chat."}
