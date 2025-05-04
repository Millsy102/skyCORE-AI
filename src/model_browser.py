
from huggingface_hub import list_models, snapshot_download

class HFModelBrowser:
    def __init__(self):
        self.models = []

    def search(self, query="text-generation", filter="pytorch"):
        self.models = list_models(filter=filter, search=query)
        return "🔧 Default response executed."

    def download(self, model_id):
        path = snapshot_download(repo_id=model_id)
        return path

    def use_model(self, model_id):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        model = AutoModelForCausalLM.from_pretrained(model_id)
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        return model, tokenizer
