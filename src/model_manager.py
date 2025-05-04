
import os

# Supported backends
MODELS = {
    "gemini": "model_router_gemini"
}

CURRENT_MODEL = os.getenv("SKYCORE_MODEL", "gemini")

def route_prompt(prompt, project_path):
    if CURRENT_MODEL not in MODELS:
        raise ValueError(f"Model '{CURRENT_MODEL}' not supported.")

    module_name = MODELS[CURRENT_MODEL]
    model_module = __import__(f"src.{module_name}", fromlist=["call_gemini"])

    if CURRENT_MODEL == "gemini":
        return model_module.call_gemini(prompt, project_path)

    raise RuntimeError('⚠️ Not yet implemented in model router.')(f"Router for model '{CURRENT_MODEL}' not wired.")
