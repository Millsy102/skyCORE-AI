
from threading import Thread

class ActionRouter:
    def __init__(self, runtime):
        self.runtime = runtime

    def execute(self, action, value):
        try:
            if action == "switch_persona":
                self.runtime.persona.set(value)
                return f"✅ Persona switched to {value}"
            elif action == "run_plugin":
                return self.runtime.plugin_executor.run(value)
            elif action == "save_memory":
                self.runtime.memory.save()
                return "✅ Memory saved"
            elif action == "load_snapshot":
                return self.runtime.memory.load_snapshot(value)
            elif action == "train_model":
                # Simulate training
                Thread(target=lambda: print('Thread running')).start()
                return f"🚀 Training model with {value}"
        except Exception as e:
            return f"❌ Error: {e}"
        return "⚠️ Unknown action"
