
from src.plugin_config_parser import PluginConfigParser
import os

class SettingsBridge:
    def __init__(self, plugins_dir='plugins'):
        self.plugins_dir = plugins_dir
        self.settings_cache = {}

    def load_all_plugin_settings(self):
        plugin_settings = {}
        for plugin in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, plugin)
            if not os.path.isdir(plugin_path):
                continue
            parser = PluginConfigParser(plugin_path)
            config = parser.parse()
            plugin_settings[plugin] = config
            self.settings_cache[plugin] = config
        return plugin_settings

    def get_settings_for_plugin(self, plugin_name):
        return self.settings_cache.get(plugin_name, {})

    def update_setting(self, plugin_name, key, value):
        if plugin_name not in self.settings_cache:
            return False
        self.settings_cache[plugin_name][key] = value
        return True
