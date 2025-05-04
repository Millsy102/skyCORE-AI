import os
import subprocess
import requests
import zipfile
import shutil

class AutoInstallHandler:
    def __init__(self, plugin_path="plugins"):
        self.plugin_path = plugin_path
        os.makedirs(self.plugin_path, exist_ok=True)

    def install_from_github_zip(self, zip_url, plugin_name):
        zip_path = f"{self.plugin_path}/{plugin_name}.zip"
        folder_path = f"{self.plugin_path}/{plugin_name}"
        try:
            r = requests.get(zip_url)
            with open(zip_path, "wb") as f:
                f.write(r.content)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(folder_path)
            os.remove(zip_path)
            return f"✅ Installed {plugin_name} from GitHub ZIP"
        except Exception as e:
            return f"❌ Failed: {e}"

    def pip_install(self, package_name):
        try:
            subprocess.check_call(["pip", "install", package_name])
            return f"📦 Installed {package_name} via pip"
        except Exception as e:
            return f"❌ pip install failed: {e}"

    def clone_git_repo(self, git_url, plugin_name=None):
        if not plugin_name:
            plugin_name = git_url.strip("/").split("/")[-1].replace(".git", "")
        dest = os.path.join(self.plugin_path, plugin_name)
        try:
            subprocess.check_call(["git", "clone", git_url, dest])
            return f"✅ Cloned {plugin_name} from Git"
        except Exception as e:
            return f"❌ Git clone failed: {e}"

    def is_plugin_valid(self, plugin_name):
        plugin_file = os.path.join(self.plugin_path, plugin_name, "plugin.py")
        return os.path.exists(plugin_file)

    def try_register_plugin(self, runtime, plugin_name):
        if self.is_plugin_valid(plugin_name):
            from src.plugin_loader import PluginLoader
            runtime.plugins = PluginLoader().plugins
            return f"🔁 Registered plugin: {plugin_name}"
        return f"⚠️ Plugin '{plugin_name}' is not valid"
