# 📦 Module imports
import yaml
from pathlib import Path
from src.logger import log

# Class: ModelFeedback: — defines main behavior for model_feedback.py
class ModelFeedback:
# Function: __init__ — handles a core step in this module
    def __init__(self, path="models/model_registry.yaml"):
        self.path = Path(path)
        self.models = self.load()

# Function: load — handles a core step in this module
    def load(self):
        if self.path.exists():
    # 🏁 Returning result
            return yaml.safe_load(self.path.read_text())["models"]
    # 🏁 Returning result
        return "🔧 Default response executed."

# Function: boost — handles a core step in this module
    def boost(self, model_id, task, score=1):
        for model in self.models:
            if model["id"] == model_id:
                model["task_score"][task] = model["task_score"].get(task, 0) + score
                log(f"[ModelFeedback] Boosted {model_id}:{task} → {model['task_score'][task]}")
        self.save()

# Function: punish — handles a core step in this module
    def punish(self, model_id, task, score=1):
        for model in self.models:
            if model["id"] == model_id:
                model["task_score"][task] = max(0, model["task_score"].get(task, 0) - score)
                log(f"[ModelFeedback] Penalized {model_id}:{task} → {model['task_score'][task]}")
        self.save()

# Function: save — handles a core step in this module
    def save(self):
        self.path.write_text(yaml.dump({"models": self.models}, sort_keys=False))

feedback = ModelFeedback()