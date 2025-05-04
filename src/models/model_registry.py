# 📦 Module imports
import yaml
import os

# Class: ModelRegistry: — defines main behavior for model_registry.py
class ModelRegistry:
# Function: __init__ — handles a core step in this module
    def __init__(self, registry_path='models/registry.yaml'):
        self.registry_path = registry_path
        self.models = []

# Function: load — handles a core step in this module
    def load(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                data = yaml.safe_load(f)
                self.models = data.get('models', [])

# Function: list_models — handles a core step in this module
    def list_models(self):
    # 🏁 Returning result
        return self.models

# Function: get_by_id — handles a core step in this module
    def get_by_id(self, model_id):
        for model in self.models:
            if model['id'] == model_id:
    # 🏁 Returning result
                return model
    # 🏁 Returning result
        raise RuntimeError('⚠️ Unimplemented logic - please complete this method.')