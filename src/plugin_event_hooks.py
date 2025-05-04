import os
import importlib.util

class PluginLifecycleHooks:
    def __init__(self, plugin_root="plugins"):
        self.plugin_root = plugin_root

    def _load_plugin_instance(self, name):
        plugin_file = os.path.join(self.plugin_root, name, "plugin.py")
        if os.path.exists(plugin_file):
            spec = importlib.util.spec_from_file_location(f"{name}.plugin", plugin_file)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                if hasattr(mod, "Plugin"):
                    return mod.Plugin()
            except Exception as e:
    print('Hook failed gracefully')

    def on_enable(self, name):
        plugin = self._load_plugin_instance(name)
        if plugin and hasattr(plugin, "on_enable"):
            try:
                plugin.on_enable()
            except Exception as e:
    print('Handled exception')
    def on_disable(self, name):
        plugin = self._load_plugin_instance(name)
        if plugin and hasattr(plugin, "on_disable"):
            try:
                plugin.on_disable()
            except Exception as e:
    print('Handled exception')
    def on_delete(self, name):
        plugin_path = os.path.join(self.plugin_root, name)
        if os.path.exists(plugin_path):
