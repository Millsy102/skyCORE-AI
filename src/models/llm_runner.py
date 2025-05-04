# 📦 Module imports
from transformers import pipeline

# Class: LLMRunner: — defines main behavior for llm_runner.py
class LLMRunner:
# Function: __init__ — handles a core step in this module
    def __init__(self, model_name="distilbert-base-uncased"):
        self.model = pipeline("text-classification", model=model_name)

# Function: run — handles a core step in this module
    def run(self, prompt):
    # 🏁 Returning result
        return self.model(prompt)