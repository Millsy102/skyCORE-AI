# 📦 Module imports
import requests
from src.vault_manager import vault
from src.logger import log

# Class: HuggingFaceModelEngine: — defines main behavior for huggingface_model_engine.py
class HuggingFaceModelEngine:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.api_key = vault.get("huggingface_token")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

# Function: infer — handles a core step in this module
    def infer(self, model_id, prompt, parameters=None):
        url = f"https://api-inference.huggingface.co/models/{model_id}"
        data = {"inputs": prompt}
        if parameters:
            data["parameters"] = parameters

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
    # 🏁 Returning result
            return result[0]["generated_text"] if isinstance(result, list) else result
        except Exception as e:
            log(f"[HuggingFaceEngine] Error calling {model_id}: {e}")
    # 🏁 Returning result
            return f"[ERROR] {e}"

hf_engine = HuggingFaceModelEngine()