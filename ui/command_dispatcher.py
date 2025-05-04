
from src.slash_command_extender import handle_extended_slash
from src.natural_router import interpret_natural_input

def process_gui_input(user_text, project_path):
    resolved = user_text if user_text.startswith("/") else interpret_natural_input(user_text)
    response = handle_extended_slash(resolved, project_path)
    return f"🧠 Understood as `{resolved}`\n\n{response}"
