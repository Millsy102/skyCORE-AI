
import os
import requests

class GitHubPluginLoader:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        os.makedirs(plugin_dir, exist_ok=True)

    def fetch(self, url):
        name = url.split("/")[-2] if "github" in url else "plugin"
        path = os.path.join(self.plugin_dir, name)
        os.makedirs(path, exist_ok=True)
        r = requests.get(url)
        if r.status_code == 200:
            with open(os.path.join(path, "main.py"), "w") as f:
                f.write(r.text)
            return f"✅ Plugin '{name}' installed."
        return "❌ Failed to fetch plugin."
