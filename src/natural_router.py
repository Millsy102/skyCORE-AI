
# Converts plain English input into internal slash commands
import re

def interpret_natural_input(text):
    text = text.strip().lower()

    if "generate a plugin" in text or "make a plugin" in text:
        return f"/ai {text}"

    if text.startswith("summarize") or "what has it done" in text:
        return "/summary"

    if "switch to" in text and "model" in text:
        model = text.split("switch to")[-1].strip().split()[0]
        return f"/model {model}"

    if "edit" in text or "refactor" in text:
        # assume they're editing a file
        match = re.search(r"(edit|refactor) (.+\.py)", text)
        if match:
            action = match.group(1)
            path = match.group(2)
            return f"/file {path} {action}"
        return f"/ai {text}"

    if "list plugins" in text:
        return "/plugin list"

    return f"/ai {text}"  # default fallback
