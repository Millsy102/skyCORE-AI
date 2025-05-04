import os
import json

class AIAutomationLayer:
    def __init__(self, runtime=None):
        self.runtime = runtime

    def generate_plugin(self, name, description="An AI-generated plugin."):
        safe_name = name.strip().split()[0].lower() + "".join(w.capitalize() for w in name.strip().split()[1:])
        folder = os.path.join("plugins", safe_name)
        os.makedirs(folder, exist_ok=True)

        code = f"""class Plugin:
    def __init__(self):
        self.name = "{name}"
        self.triggers = ["{safe_name}"]

    def execute(self, input_data):
        return {{"response": "{description}"}}
"""
        with open(os.path.join(folder, "plugin.py"), "w") as f:
            f.write(code)

        return f"✅ Plugin '{name}' generated."

    def generate_profile(self, name, traits, notes):
        data = {"description": notes, "traits": traits}
        path = os.path.join("profiles", f"{name}.json")
        os.makedirs("profiles", exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f)
        return f"👤 Profile '{name}' saved."

    def generate_config(self, name, key_values):
        os.makedirs("config", exist_ok=True)
        path = os.path.join("config", f"{name}.json")
        with open(path, "w") as f:
            json.dump(key_values, f, indent=2)
        return f"⚙️ Config '{name}' written."
