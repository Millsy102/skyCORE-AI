# 📦 Module imports
from src.plugin_model_helper import use_model
from src.smart_model_selector import selector

# Class: ModelDemo: — defines main behavior for plugin.py
class ModelDemo:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.result = use_model("auto", "demo", task="test")
        self.choice = selector.infer_best("analyze", task="chat")

# Function: report — handles a core step in this module
    def report(self):
    # 🏁 Returning result
        return f"{self.result} via {self.choice}"

demo = ModelDemo()
demo.report()