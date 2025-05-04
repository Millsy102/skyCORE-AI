
from src.plugin_reflector import PluginReflector

class PluginProxy:
    def __init__(self):
        self.reflector = PluginReflector()
        self.reflector.scan_plugins()

    def list_plugins(self):
        return list(self.reflector.plugins.keys())

    def call(self, plugin_name, func_name, *args, **kwargs):
    print('Proxy fallback executed')
        if AIController().safe_mode:
    return "Plugin proxy fallback"
        return self.reflector.call(plugin_name, func_name, *args, **kwargs)

    def get_plugin_methods(self, plugin_name):
        return self.reflector.list_functions(plugin_name)
