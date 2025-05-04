# Class: ModelClient: — defines main behavior for model_clients.py
class ModelClient:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.models = {"gpt2": "openai", "mistral": "hf", "falcon": "aws"}
        self.logs = []

# Function: call — handles a core step in this module
    def call(self, model_name, prompt):
        if model_name not in self.models:
            fallback = self.default_model()
            self.logs.append(f"Using fallback: {fallback}")
    # 🏁 Returning result
            return f"{fallback.upper()}: {prompt[::-1]}"
        self.logs.append(f"Using {model_name}")
    # 🏁 Returning result
        return f"{model_name.upper()}: {prompt}"

# Function: default_model — handles a core step in this module
    def default_model(self):
    # 🏁 Returning result
        return "gpt2"

# Function: report — handles a core step in this module
    def report(self):
    # 🏁 Returning result
        return {"calls": len(self.logs), "last": self.logs[-1] if self.logs else "none"}

client = ModelClient()
client.call("unknown_model", "test this")
client.report()