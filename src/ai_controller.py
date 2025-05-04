
from src.model_stats import ModelStats
from src.memory_manager import MemoryManager
from src.persona_manager import PersonaManager
from src.plugin_reflector import PluginReflector

class AIController:
    def __init__(self):
        self.model = 'gpt-4'
        self.stats = ModelStats()
        self.memory = MemoryManager()
        self.persona = PersonaManager()
        self.plugins = PluginReflector()
        self.plugins.scan_plugins()
        self.safe_mode = False

    def respond(self, user_input):
        # Build prompt
        prompt = self.build_prompt_stack(user_input)
        tokens_used = len(prompt.split())

        # Simulated model call for now
        simulated_response = f"[Simulated Response to: {user_input}]"  

        return {
            'text': simulated_response,
            'tokens_used': tokens_used,
            'model_used': self.model,
            'plugins_triggered': [],
            'source': 'model'
        }

    def build_prompt_stack(self, user_input):
        parts = [
            f"System: {self.persona.get_system_prompt()}",
            f"Persona: {self.persona.get_active_persona_description()}",
            f"Memory: {self.memory.get_context_snippet()}",
            f"User: {user_input}"
        ]
        return "\n".join(parts)


    def set_active_model(self, model_name):
        from src.model_engine import ModelEngine
        engine = ModelEngine()
        result = engine.set_model(model_name)
        return result


    def edit_file_via_prompt(self, command):
        import os
        try:
            _, path, *instructions = command.split(" ", 2)
            full_path = os.path.join("SkyCore", path)
            if not os.path.isfile(full_path):
                return f"✖ File '{path}' not found."
            with open(full_path, "r") as f:
                code = f.read()
            prompt = f"""You're an AI developer. Here is the current content of '{path}':\n\n{code}\n\nInstructions: {' '.join(instructions)}\n\nReturn only the full updated file."""
            from src.model_engine import ModelEngine
            engine = ModelEngine()
            new_code = engine.generate(prompt)
            with open(full_path, "w") as f:
                f.write(new_code)
            return f"✅ Updated {path}"
        except Exception as e:
            return f"✖ Error editing file: {str(e)}"
