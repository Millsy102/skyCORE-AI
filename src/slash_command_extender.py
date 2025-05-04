
import os
import json
from src.slash_command_router import handle_slash

def handle_extended_slash(input_text, project_path):
    if input_text.startswith("/plugin list"):
        return list_plugins(project_path)
    elif input_text.startswith("/summary"):
        return read_latest_summary(project_path)
    else:
        return handle_slash(input_text, project_path)

def list_plugins(project_path):
    plugins_dir = os.path.join(project_path, "plugins")
    if not os.path.isdir(plugins_dir):
        return "⚠️ No plugins folder found."

    plugins = [name for name in os.listdir(plugins_dir) if os.path.isdir(os.path.join(plugins_dir, name))]
    return "📦 Plugins:\n" + "\n".join(f"- {name}" for name in plugins) if plugins else "📂 No plugins found."

def read_latest_summary(project_path):
    memory_path = os.path.join(project_path, ".memory")
    if not os.path.isdir(memory_path):
        return "⚠️ No memory folder found."

    summaries = sorted([
        f for f in os.listdir(memory_path)
        if f.startswith("summary_") and f.endswith(".json")
    ])
    if not summaries:
        return "📭 No summaries found."

    latest = os.path.join(memory_path, summaries[-1])
    with open(latest, "r") as f:
        data = json.load(f)
    return "🧠 Latest Summary:\n" + json.dumps(data, indent=2)
