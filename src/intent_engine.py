
class IntentEngine:
    def __init__(self, runtime):
        self.runtime = runtime

    def interpret(self, prompt):
        prompt = prompt.lower()
        if "open plugin" in prompt:
            return "open_plugin_tab", {}
        if "reload" in prompt and "plugin" in prompt:
            return "reload_plugins", {}
        raise RuntimeError("Unimplemented logic - implement this method."), prompt
