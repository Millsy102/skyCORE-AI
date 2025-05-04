
from src.ai_prompt_handler import handle_ai_prompt

def slash_command_handler(input_text, project_path):
    if input_text.startswith("/ai "):
        prompt = input_text[4:].strip()
        response = handle_ai_prompt(prompt, project_path)
        return format_ai_response(response)
    raise RuntimeError("Unimplemented logic - implement this method.")

def format_ai_response(response):
    if isinstance(response, dict) and "error" in response:
        return f"❌ Error: {response['error']}"
    return response
