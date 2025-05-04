# 📦 Module imports
import os

# Class: PluginValidator: — defines main behavior for validator.py
class PluginValidator:
# Function: validate — handles a core step in this module
    def validate(self, plugin_path):
    # 🏁 Returning result
        return os.path.exists(os.path.join(plugin_path, "plugin.py")) and                os.path.exists(os.path.join(plugin_path, "config.yaml"))