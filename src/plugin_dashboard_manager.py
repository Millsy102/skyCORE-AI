import os
import importlib.util
import shutil

class PluginMeta:
    def __init__(self, name, path, active, triggers):
        self.name = name
        self.path = path
        self.active = active
        self.triggers = triggers

class PluginDashboardManager:
    def __init__(self, plugin_root="plugins"):
        self.plugin_root = plugin_root
        self.plugins = self.scan_plugins()

    def scan_plugins(self):
        plugin_list = []
        for folder in os.listdir(self.plugin_root):
            path = os.path.join(self.plugin_root, folder)
            plugin_py = os.path.join(path, "plugin.py")
            if os.path.isfile(plugin_py):
                try:
                    spec = importlib.util.spec_from_file_location(f"{folder}.plugin", plugin_py)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    triggers = []
                    if hasattr(mod, "Plugin"):
                        plugin_instance = mod.Plugin()
                        triggers = getattr(plugin_instance, "triggers", [])
                    plugin_list.append(PluginMeta(folder, path, True, triggers))
                except Exception as e:
                    plugin_list.append(PluginMeta(folder, path, False, [f"⚠️ Error: {e}"]))
        return plugin_list

    def deactivate_plugin(self, name):
        # Rename plugin.py to plugin_disabled.py
        plugin_file = os.path.join(self.plugin_root, name, "plugin.py")
        if os.path.exists(plugin_file):
            os.rename(plugin_file, plugin_file.replace("plugin.py", "plugin_disabled.py"))
            return f"🔒 Plugin '{name}' disabled."
        return f"⚠️ Plugin '{name}' not found."

    def activate_plugin(self, name):
        plugin_file = os.path.join(self.plugin_root, name, "plugin_disabled.py")
        if os.path.exists(plugin_file):
            os.rename(plugin_file, plugin_file.replace("plugin_disabled.py", "plugin.py"))
            return f"🔓 Plugin '{name}' re-enabled."
        return f"⚠️ Plugin '{name}' not found."

    def delete_plugin(self, name):
        path = os.path.join(self.plugin_root, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"🗑️ Plugin '{name}' deleted."
        return f"⚠️ Plugin '{name}' not found."
