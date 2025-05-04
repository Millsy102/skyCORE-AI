# 📦 Module imports
import subprocess
import os
from src import settings_core

INSTALLED_PLUGINS = set()

# Function: install_plugin_requirements — handles a core step in this module
def install_plugin_requirements(plugin_path):
    settings = settings_core.load_settings()
    if not settings.get("allow_plugin_installs", True):
    # 🏁 Returning result
        return

    if plugin_path in INSTALLED_PLUGINS:
    # 🏁 Returning result
        return  # Already installed this round

    req_path = os.path.join(plugin_path, "requirements.txt")
    if os.path.exists(req_path):
        try:
            subprocess.check_call(["pip", "install", "-r", req_path])
        except subprocess.CalledProcessError as e:
    print('Install failure')
