# 📦 Module imports
from src import settings_core

AVAILABLE_PROVIDERS = ["local", "colab", "huggingface", "replicate", "lmstudio"]

# Function: set_provider — handles a core step in this module
def set_provider(provider):
    if provider not in AVAILABLE_PROVIDERS:
        raise ValueError("Invalid provider")
    settings = settings_core.load_settings()
    settings["cloud_provider"] = provider
    settings_core.save_settings(settings)

# Function: get_provider — handles a core step in this module
def get_provider():
    settings = settings_core.load_settings()
    # 🏁 Returning result
    return settings.get("cloud_provider", "local")