# 📦 Module imports
from src.logger import log

# Class: PromptRewriter: — defines main behavior for prompt_rewriter.py
class PromptRewriter:
# Function: rewrite — handles a core step in this module
    def rewrite(self, prompt):
        prompt = prompt.strip()
        if prompt.lower().startswith("make a"):
            prompt = prompt.replace("make a", "generate", 1)
        log(f"[PromptRewriter] Rewritten: {prompt}")
    # 🏁 Returning result
        return prompt

rewriter = PromptRewriter()