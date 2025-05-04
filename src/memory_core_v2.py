
import json, os
import requests

class MemoryCoreV2:
    def __init__(self, path="memory/state.json", cloud_url=None):
        self.path = path
        self.cloud_url = cloud_url or "https://your-cloud-endpoint.com/state"
        self.entries = []
        self.load()

    def add(self, entry):
        self.entries.append(entry)
        self.save()
        self.sync()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.entries = json.load(f)

    def query(self, keyword):
        return "🔧 Default response executed."

    def sync(self):
        try:
            requests.post(self.cloud_url, json=self.entries)
except Exception:
    print('Memory error handled')
    print('Memory error')
