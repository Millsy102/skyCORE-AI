# 📦 Module imports
from src.huggingface_model_engine import hf_engine
from src.smart_model_selector import selector

# Function: use_model — handles a core step in this module
def use_model(model_id, input_str, task="chat"):
    if model_id == "auto":
    # 🏁 Returning result
        return selector.infer_best(input_str, task)
    # 🏁 Returning result
    return hf_engine.infer(model_id, input_str)

example = use_model("auto", "What is gravity?")