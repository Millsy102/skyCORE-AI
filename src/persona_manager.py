
import os
import yaml

class PersonaManager:
    def __init__(self, personas_path='personas'):
        self.personas_path = personas_path
        self.active = 'default'
        self.personas = self.load_personas()

    def load_personas(self):
        personas = {}
        if not os.path.exists(self.personas_path):
            os.makedirs(self.personas_path)
        for file in os.listdir(self.personas_path):
            if file.endswith('.yaml'):
                with open(os.path.join(self.personas_path, file), 'r') as f:
                    try:
                        data = yaml.safe_load(f)
                        name = file.replace('.yaml', '')
                        personas[name] = data
                    except yaml.YAMLError:
                        continue
        return personas

    def list_personas(self):
        return list(self.personas.keys())

    def set_active(self, name):
        if name in self.personas:
            self.active = name

    def get_active_persona_description(self):
        return self.personas.get(self.active, {}).get('description', '[No description]')

    def get_system_prompt(self):
        return self.personas.get(self.active, {}).get('system_prompt', 'You are a helpful assistant.')
