# 📦 Module imports
from transformers import pipeline

# Class: ModelManager: — defines main behavior for model_manager.py
class ModelManager:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.loaded_model = None
        self.model_id = None

# Function: load_model — handles a core step in this module
    def load_model(self, model_id):
        try:
            self.loaded_model = pipeline("text-generation", model=model_id)
            self.model_id = model_id
    # 🏁 Returning result
            return f"Model {model_id} loaded."
        except Exception as e:
    # 🏁 Returning result
            return f"[Error loading model] {e}"

# Function: run — handles a core step in this module
    def run(self, prompt):
        if not self.loaded_model:
    # 🏁 Returning result
            return "No model loaded."
        try:
            result = self.loaded_model(prompt, max_length=50, do_sample=True)
    # 🏁 Returning result
            return result[0]['generated_text']
        except Exception as e:
    # 🏁 Returning result
            return f"[Error during generation] {e}"