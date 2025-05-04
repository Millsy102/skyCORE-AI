# 📦 Module imports
import time
from src.model_router import model_router
from src.logger import log

# Class: ModelTester: — defines main behavior for model_tester.py
class ModelTester:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.results = []

# Function: run — handles a core step in this module
    def run(self, prompt="What is skyCORE-AI?", provider="openai"):
        start = time.time()
        try:
            result = model_router.route_prompt(prompt, provider=provider)
            elapsed = time.time() - start
            log(f"[ModelTester] {provider} took {elapsed:.2f}s")
            self.results.append({"provider": provider, "time": elapsed})
    # 🏁 Returning result
            return {"result": result, "time": elapsed}
        except Exception as e:
            log(f"[ModelTester] ERROR: {e}")
    # 🏁 Returning result
            return {"error": str(e)}

tester = ModelTester()