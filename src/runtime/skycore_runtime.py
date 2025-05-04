
from settings_core import SettingsCore
from memory_core import MemoryCore
from plugin_loader import PluginLoader
from ai_controller import AIController
from model_router import ModelRouter
from intent_engine import IntentEngine

class SkyCoreRuntime:
    def __init__(self):

        # Primary runtime systems
        self.settings = SettingsCore(self)
        self.memory = MemoryCore(self)
        self.plugin_loader = PluginLoader(self)
        self.ai_controller = AIController(self)
        self.model_router = ModelRouter(self)
        self.intent_engine = IntentEngine(self)

        # Optional structure
        self.tabs = {}
        self.models = {}
        self.plugins = {}
        self.personas = {}
        self.state = {}
        self.logger = self.default_logger

    def start(self):
        self.plugin_loader.load_plugins()

    def default_logger(self, msg):
