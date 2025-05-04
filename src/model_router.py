
class ModelRouter:
    def __init__(self, runtime):
        self.runtime = runtime
        self.current_model = None

    def route(self, prompt):
        if "summarize" in prompt:
            return "gpt-4"
        elif "generate code" in prompt:
            return "phi-2"
        return "default-model"

    def switch_model(self, model_id):
        self.current_model = model_id
