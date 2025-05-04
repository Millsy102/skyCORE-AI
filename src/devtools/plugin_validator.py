# 📦 Module imports
from pathlib import Path

# Class: PluginValidator: — defines main behavior for plugin_validator.py
class PluginValidator:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.valid = []
        self.invalid = []

# Function: validate — handles a core step in this module
    def validate(self, path):
        if not path.endswith("plugin.py"):
            self.invalid.append(path)
    # 🏁 Returning result
            return False
        if " " in path or not path.startswith("plugins/"):
            self.invalid.append(path)
    # 🏁 Returning result
            return False
        self.valid.append(path)
    # 🏁 Returning result
        return True

# Function: report — handles a core step in this module
    def report(self):
    # 🏁 Returning result
        return {
            "valid": self.valid,
            "invalid": self.invalid,
            "total": len(self.valid) + len(self.invalid)
        }

v = PluginValidator()
v.validate("plugins/ai_helper/plugin.py")
v.validate("bad/plugin.py")
v.report()