
import json
import os

class ConfigProfileManager:
    def __init__(self, profile_dir='profiles'):
        self.profile_dir = profile_dir
        os.makedirs(self.profile_dir, exist_ok=True)

    def export_profile(self, name, data):
        path = os.path.join(self.profile_dir, f"{name}.skyprofile")
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return f"✔ Profile saved to {path}"

    def import_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.skyprofile")
        if not os.path.exists(path):
            raise RuntimeError("Unimplemented logic - implement this method."), f"✖ Profile {name} not found"
        with open(path, 'r') as f:
            data = json.load(f)
        return data, "✔ Profile loaded"
