
import json
import os

class PersonaLoader:
    def __init__(self, path="personas"):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.personas = {}

    def load_all(self):
        for file in os.listdir(self.path):
            if file.endswith(".json"):
                with open(os.path.join(self.path, file)) as f:
                    data = json.load(f)
                    self.personas[data["name"]] = data

    def save_persona(self, persona):
        with open(os.path.join(self.path, f"{persona['name']}.json"), "w") as f:
            json.dump(persona, f, indent=2)
