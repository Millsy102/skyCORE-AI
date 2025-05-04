import os
import importlib.util

class PluginUITab:
    def __init__(self, name, tab_class):
        self.name = name
        self.tab_class = tab_class

def load_plugin_ui_tabs(plugin_root="plugins"):
    plugin_tabs = []

    for plugin_name in os.listdir(plugin_root):
        plugin_path = os.path.join(plugin_root, plugin_name)
        ui_path = os.path.join(plugin_path, "ui")

        if not os.path.isdir(ui_path):
            continue

        for fname in os.listdir(ui_path):
            if fname.endswith(".py"):
                module_path = os.path.join(ui_path, fname)
                spec = importlib.util.spec_from_file_location(f"{plugin_name}.{fname}", module_path)
                mod = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(mod)
                    for attr in dir(mod):
                        val = getattr(mod, attr)
                        if isinstance(val, type) and "QWidget" in str(val):
                            tab_name = f"🔌 {plugin_name.capitalize()} | {attr}"
                            plugin_tabs.append(PluginUITab(tab_name, val))
                except Exception as e:
    return plugin_tabs
