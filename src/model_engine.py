class ModelEngine:
    def __init__(self):
        self.active_model = "gpt-4"

    def set_model(self, model_name):
        self.active_model = model_name
        return f"🔁 Model set to: {model_name}"

    def generate(self, prompt, context=""):
        # Placeholder stub to be replaced by real API calls
        return f"🧠 [{self.active_model}] response to prompt: {prompt[:100]}..."