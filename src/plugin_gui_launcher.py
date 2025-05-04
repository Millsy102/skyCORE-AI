import os
import subprocess
import importlib.util

class PluginGUILauncher:
    def __init__(self, plugin_root="plugins"):
        self.plugin_root = plugin_root

    def launch_gui(self, plugin_name):
        plugin_path = os.path.join(self.plugin_root, plugin_name)
        plugin_file = os.path.join(plugin_path, "plugin.py")
        if not os.path.exists(plugin_file):
            return f"⚠️ Plugin {plugin_name} not found."

        spec = importlib.util.spec_from_file_location(f"{plugin_name}.plugin", plugin_file)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            if hasattr(mod, "Plugin"):
                plugin = mod.Plugin()
                gui = getattr(plugin, "gui_entry", None)
                engine = getattr(plugin, "gui_engine", "subprocess")
                if gui:
                    gui_path = os.path.join(plugin_path, gui)
                    if os.path.exists(gui_path):
                        subprocess.Popen(["python", gui_path])
                        return f"✅ GUI for {plugin_name} launched with {engine}."
                    else:
                        return f"❌ GUI entry file not found: {gui}"
                else:
                    return f"⚠️ No GUI entry defined for {plugin_name}."
        except Exception as e:
            return f"❌ Failed to launch plugin GUI: {e}"
