
class PromptStackBuilder:
    def __init__(self, system_prompt, persona_description, memory_snippet, user_input):
        self.system = system_prompt
        self.persona = persona_description
        self.memory = memory_snippet
        self.input = user_input

    def build(self):
        return f"""System: {self.system}
Persona: {self.persona}
Memory: {self.memory}
User: {self.input}"""
