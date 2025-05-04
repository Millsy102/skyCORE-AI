
import os
import yaml

def load_rules(project_path):
    rules_path = os.path.join(project_path, ".rules")
    if not os.path.exists(rules_path):
        return {}

    try:
        with open(rules_path, "r") as f:
            rules = yaml.safe_load(f) or {}
            return rules
    except Exception as e:
        return {"error": str(e)}

def apply_rules_to_prompt(prompt, rules):
    if "context_files" in rules:
        context_text = []
        for path in rules["context_files"]:
            full_path = os.path.join(os.getcwd(), path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    context_text.append(f"// Context from {path}:\n{f.read()}\n")
            except Exception:
                continue
        return "\n".join(context_text) + "\n\n" + prompt
    return prompt
