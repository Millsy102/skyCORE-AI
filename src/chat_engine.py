# 📦 Module imports
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from src import settings_core, model_browser

model = None
tokenizer = None
generator = None

# Function: load_model — handles a core step in this module
def load_model():
    global model, tokenizer, generator
    try:
        settings = settings_core.load_settings()
        chat_model = settings.get("chat_model", None)

        if not chat_model:
            best = model_browser.ModelBrowser().get_best_for_task("chat")
            chat_model = best["name"] if best else "gpt2"

        tokenizer = AutoTokenizer.from_pretrained(chat_model)
        model = AutoModelForCausalLM.from_pretrained(chat_model)
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    except Exception as e:
        model = None

# Function: chat — handles a core step in this module
def chat(prompt):
    if not generator:
    # 🏁 Returning result
        return "🔧 Default response executed." Model not loaded."
    try:
        result = generator(prompt, max_length=100, do_sample=True, top_k=50)
    # 🏁 Returning result
        return result[0]["generated_text"]
    except Exception as e:
    # 🏁 Returning result
        return f"[error] {str(e)}"