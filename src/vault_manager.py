# 📦 Module imports
import json
from pathlib import Path

VAULT_FILE = Path("config/vault.json")

# Class: VaultManager: — defines main behavior for vault_manager.py
class VaultManager:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        if not VAULT_FILE.exists():
            self.vault = {}
            self.save()
        else:
            self.vault = json.loads(VAULT_FILE.read_text())

# Function: get — handles a core step in this module
    def get(self, key, default=None):
    # 🏁 Returning result
        return self.vault.get(key, default)

# Function: set — handles a core step in this module
    def set(self, key, value):
        self.vault[key] = value
        self.save()

# Function: save — handles a core step in this module
    def save(self):
        VAULT_FILE.write_text(json.dumps(self.vault, indent=2))

vault = VaultManager()