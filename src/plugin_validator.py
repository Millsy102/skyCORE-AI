
import os
import yaml

class PluginValidator:
    def __init__(self, plugins_path='plugins'):
        self.plugins_path = plugins_path

    def validate(self):
        results = []
        for folder in os.listdir(self.plugins_path):
            plugin_dir = os.path.join(self.plugins_path, folder)
            if not os.path.isdir(plugin_dir):
                continue

            main_path = os.path.join(plugin_dir, 'main.py')
            config_path = os.path.join(plugin_dir, 'config.yaml')
            ui_path = os.path.join(plugin_dir, 'ui.yaml')

            plugin_result = [f"[Plugin: {folder}]"]

            if os.path.exists(main_path):
                plugin_result.append("✔ main.py exists")
            else:
                plugin_result.append("✖ Missing main.py")

            if os.path.exists(config_path):
                plugin_result.append("✔ config.yaml exists")
                try:
                    with open(config_path, 'r') as f:
                        yaml.safe_load(f)
                    plugin_result.append("✔ config.yaml is valid YAML")
                except yaml.YAMLError as e:
                    plugin_result.append(f"✖ config.yaml has YAML error: {e}")
            else:
                plugin_result.append("✖ Missing config.yaml")

            if os.path.exists(ui_path):
                plugin_result.append("✔ ui.yaml exists")
            else:
                plugin_result.append("⚠ ui.yaml not found (optional)")

            results.append("\n".join(plugin_result))

        return "\n\n".join(results)
