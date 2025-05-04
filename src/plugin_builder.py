
import os
import re

def extract_plugin_from_response(text, plugin_name="autoplugin"):
    plugin_root = os.path.join("plugins", plugin_name)
    os.makedirs(plugin_root, exist_ok=True)

    code_blocks = re.findall(r"```(?:[a-z]+)?\n(.*?)```", text, re.DOTALL)
    filenames = re.findall(r"# ?File: ?(\S+)", text)

    for i, block in enumerate(code_blocks):
        filename = filenames[i] if i < len(filenames) else f"snippet_{i}.py"
        filepath = os.path.join(plugin_root, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(block.strip())

    return f"✅ Plugin created: {plugin_root} with {len(code_blocks)} file(s)"
