import os
import json

class CloudConfigStore:
    def __init__(self, config_path="config/skycore_cloud.json"):
        self.path = config_path
        self._data = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=2)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def get(self, key, default=None):
        return self._data.get(key, default)
