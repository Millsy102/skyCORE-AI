
import os
from src.dashboard_ai_hook import slash_command_handler
from src.file_diff import generate_diff_preview
from src.agent_log import AgentLog

AVAILABLE_MODELS = ["gemini"]

def handle_slash(input_text, project_path):
    input_text = input_text.strip()
    if input_text.startswith("/model "):
        model = input_text.split(" ", 1)[-1].strip()
        if model not in AVAILABLE_MODELS:
            return f"⚠️ Model '{model}' is not available."
        os.environ["SKYCORE_MODEL"] = model
        return f"✅ Model switched to: {model}"

    elif input_text.startswith("/ai "):
        return slash_command_handler(input_text, project_path)

    elif input_text.startswith("/file "):
        return handle_file_command(input_text, project_path)

    return "❓ Unknown command."

def handle_file_command(input_text, project_path):
    try:
        parts = input_text.split(" ", 3)
        _, _, file_path, action = parts
        abs_path = os.path.join(project_path, file_path)
        log = AgentLog(project_path)

        if not os.path.exists(abs_path):
            return f"❌ File not found: {file_path}"
        with open(abs_path, "r", encoding="utf-8") as f:
            original = f.read()

        log.log_step("file", "Loaded original file", {"path": file_path})
        prompt = f"Please {action} in the following file:\n\n{original}"
        response = slash_command_handler(f"/ai {prompt}", project_path)

        if isinstance(response, dict) and "error" in response:
            log.log_step("error", "AI error during file edit", {"error": response["error"]})
            log.save_log("file")
            return response["error"]

        new_code = response if isinstance(response, str) else str(response)
        diff_preview = generate_diff_preview(original, new_code, file_path)
        log.log_step("diff", "Generated file diff", {"preview": diff_preview[:1000]})
        log.save_log("file")

        return f"📝 Preview of changes to `{file_path}`:\n\n```diff\n{diff_preview}```\n\n✅ Apply manually or approve logic."
    except Exception as e:
        return f"❌ File command error: {str(e)}"
