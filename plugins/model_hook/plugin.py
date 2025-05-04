# 📦 Module imports
from src.plugin_model_helper import use_model
from src.smart_model_selector import selector

# Class: AIPlugin: — defines main behavior for plugin.py
class AIPlugin:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.result = use_model("auto", "scan", task="logic")
        self.best = selector.infer_best("choose", task="build")

# Function: output — handles a core step in this module
    def output(self):
    # 🏁 Returning result
        return f"{self.result} >> {self.best}"

p = AIPlugin()
p.output()