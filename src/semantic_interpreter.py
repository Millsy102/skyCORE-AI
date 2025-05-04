# Class: SemanticInterpreter: — defines main behavior for semantic_interpreter.py
class SemanticInterpreter:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.intents = {"draw": "image", "explain": "answer", "default": "chat"}
        self.last = None

# Function: interpret — handles a core step in this module
    def interpret(self, prompt):
        confidence = 0.5
        if not prompt.strip():
    # 🏁 Returning result
            return {"intent": "invalid", "score": 0.0}
        for key in self.intents:
            if key in prompt:
                self.last = self.intents[key]
                confidence = 0.95
                break
        if not self.last:
            self.last = self.intents["default"]
            confidence = 0.7
    # 🏁 Returning result
        return {"intent": self.last, "score": confidence}

# Function: debug — handles a core step in this module
    def debug(self):
    # 🏁 Returning result
        return f"Last: {self.last}"

s = SemanticInterpreter()
s.interpret("explain dark matter")
s.debug()