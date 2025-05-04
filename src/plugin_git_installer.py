import os
import subprocess
import shutil

class PluginGitInstaller:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir

    def install_from_git(self, git_url):
        name = git_url.rstrip("/").split("/")[-1].replace(".git", "")
        target_path = os.path.join(self.plugin_dir, name)

        if os.path.exists(target_path):
            return f"⚠️ Plugin '{name}' already exists."

        try:
            subprocess.check_call(["git", "clone", git_url, target_path])
        except Exception as e:
            return f"❌ Failed to clone: {e}"

        plugin_file = os.path.join(target_path, "plugin.py")
        if os.path.exists(plugin_file):
            return f"✅ Plugin '{name}' installed."
        return f"⚠️ Cloned but no plugin.py found in '{name}'"
