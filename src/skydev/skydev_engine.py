# Class: SkyDevEngine: — defines main behavior for skydev_engine.py
class SkyDevEngine:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.prompts = []
        self.history = []

# Function: add — handles a core step in this module
    def add(self, line):
        self.prompts.append(line)

# Function: compile — handles a core step in this module
    def compile(self):
        compiled = "\n".join(self.prompts)
        self.history.append(compiled)
    # 🏁 Returning result
        return compiled

# Function: reset — handles a core step in this module
    def reset(self):
        self.prompts.clear()

# Function: last — handles a core step in this module
    def last(self):
    # 🏁 Returning result
        return self.history[-1] if self.history else ""

engine = SkyDevEngine()
engine.add("Build plugin template")
engine.add("Add inference model")
engine.compile()
engine.last()