
class CompanionAgent:
    def __init__(self, persona):
        self.name = persona.get("name", "Unnamed")
        self.prompt = persona.get("prompt", "")
        self.voice = persona.get("voice", "Default")
        self.traits = persona.get("traits", [])
        self.memory = []

    def speak(self, input_text):
        return f"[{self.name}] {self.prompt} - Response to: {input_text}"
