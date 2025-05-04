class AgentRouter:
    def classify(self, prompt: str) -> str:
        prompt = prompt.lower()
        if prompt.startswith("/") or "run " in prompt or "open " in prompt:
            return "command"
        elif any(keyword in prompt for keyword in ["plugin", "model", "persona", "execute"]):
            return "action"
        return "chat"
