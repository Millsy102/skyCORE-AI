# 📦 Module imports
from src.prompt_stack import PromptStack
from src.logger import log

# Class: ContextBuilder: — defines main behavior for context_builder.py
class ContextBuilder:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.memory = PromptStack()

# Function: build_context — handles a core step in this module
    def build_context(self, user_input, agent="default"):
        self.memory.add(user_input)
        context = self.memory.get_recent(10)
        context_summary = "\n".join([f"{c['role']}: {c['content']}" for c in context])
        log(f"[ContextBuilder] Context built for agent '{agent}'")
    # 🏁 Returning result
        return context_summary

context_builder = ContextBuilder()