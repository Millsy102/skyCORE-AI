import zipfile, os

class PluginVault:
    def export(self, plugin_name):
        path = os.path.join("plugins", plugin_name)
        archive = f"{plugin_name}.zip"
        with zipfile.ZipFile(archive, "w") as zipf:
            for root, _, files in os.walk(path):
                for f in files:
                    abs_path = os.path.join(root, f)
                    rel = os.path.relpath(abs_path, path)
                    zipf.write(abs_path, arcname=os.path.join(plugin_name, rel))
        return archive
