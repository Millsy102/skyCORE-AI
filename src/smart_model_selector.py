# 📦 Module imports
from src.huggingface_model_engine import hf_engine

# Class: SmartModelSelector: — defines main behavior for smart_model_selector.py
class SmartModelSelector:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.model_scores = {
            "gpt2": {"chat": 4, "code": 2},
            "tiiuae/falcon-7b": {"chat": 7, "code": 5},
            "mistralai/Mistral-7B-Instruct-v0.1": {"chat": 9, "code": 8},
        }

# Function: best_model — handles a core step in this module
    def best_model(self, task="chat"):
        ranked = sorted(self.model_scores.items(), key=lambda kv: kv[1].get(task, 0), reverse=True)
    # 🏁 Returning result
        return ranked[0][0]

# Function: infer_best — handles a core step in this module
    def infer_best(self, prompt, task="chat"):
        model = self.best_model(task)
    # 🏁 Returning result
        return hf_engine.infer(model, prompt)

selector = SmartModelSelector()
selector.infer_best("Hello, world!", task="chat")