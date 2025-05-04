# 📦 Module imports
from src.settings_handler import SettingsHandler
from src.memory_manager import MemoryManager
from src.persona_manager import PersonaManager
from src.plugin_loader import PluginLoader
from src.logging_engine import log_trace
from src.model_router import ModelRouter
from src.ai_controller import AIController
from src.plugin_executor import PluginExecutor
from src.plugin_devtools import PluginDevTools
from src.command_router import CommandRouter
from src.ethical_guard import EthicalGuard
from src.plugin_schema import PluginSchemaValidator

# Class: skyCORE-AIRuntime: — defines main behavior for runtime.py
class SkyCoreRuntime:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.settings = SettingsHandler()
        self.memory = MemoryManager()
        self.persona = PersonaManager()
        self.plugin_loader = PluginLoader()
        self.plugin_executor = PluginExecutor()
        self.plugin_devtools = PluginDevTools()
        self.model_router = ModelRouter()
        self.ai_controller = AIController()
        self.command_router = CommandRouter()
        self.guard = EthicalGuard()
        self.schema = PluginSchemaValidator()

        self._initialize_runtime()

# Function: _initialize_runtime — handles a core step in this module
    def _initialize_runtime(self):
        self.plugin_loader.load_all()
        log_trace("SkyCoreRuntime", "_initialize_runtime", "init", "Runtime initialized and plugins loaded")

# Function: get_services — handles a core step in this module
    def get_services(self) -> dict:
    # 🏁 Returning result
        return {
            "settings": self.settings,
            "memory": self.memory,
            "persona": self.persona,
            "plugin_loader": self.plugin_loader,
            "plugin_executor": self.plugin_executor,
            "plugin_devtools": self.plugin_devtools,
            "model_router": self.model_router,
            "ai_controller": self.ai_controller,
            "command_router": self.command_router,
            "ethical_guard": self.guard,
            "schema_validator": self.schema
        }
