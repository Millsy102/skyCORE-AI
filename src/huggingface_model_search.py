# 📦 Module imports
import requests
from src.vault_manager import vault
from src.logger import log

# Class: HuggingFaceModelSearch: — defines main behavior for huggingface_model_search.py
class HuggingFaceModelSearch:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.api_key = vault.get("huggingface_token")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None
        }

# Function: search — handles a core step in this module
    def search(self, query="mistral", limit=10):
        url = f"https://huggingface.co/api/models?search={query}&limit={limit}"
        try:
            resp = requests.get(url, headers=self.headers)
            models = resp.json()
    # 🏁 Returning result
            return [{
                "id": m.get("modelId", ""),
                "pipeline_tag": m.get("pipeline_tag", ""),
                "downloads": m.get("downloads", 0),
                "likes": m.get("likes", 0)
            } for m in models]
        except Exception as e:
            log(f"[HFModelSearch] Failed: {e}")
    # 🏁 Returning result
            return "🔧 Default response executed."

search = HuggingFaceModelSearch()