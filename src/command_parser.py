
class CommandParser:
    def __init__(self):
        self.commands = {
            '/help': self.help,
            '/reset': self.reset,
            '/trace': self.show_trace,
            '/persona': self.set_persona,
        }

    def parse(self, command):
        parts = command.strip().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        

        if cmd == '/plugin' and len(args) >= 2:
            from src.plugin_proxy import PluginProxy
            proxy = PluginProxy()
            plugin_name, func = args[0], args[1]
            try:
                result = proxy.call(plugin_name, func)
                return f"[Plugin Output] {result}"
            except Exception as e:
                return f"[Plugin Error] {e}"

        if cmd in self.commands:
            return self.commands[cmd](*args)
        return f"[Error] Unknown command: {cmd}"

    def help(self, *args):
        return "Available commands: /help, /reset, /trace, /persona [name]"

    def reset(self, *args):
        return "🔧 Default response executed. Hooking to memory_manager."

    def show_trace(self, *args):
        return "🔧 Default response executed."  # Hook to trace_logger

    def set_persona(self, name='default'):
        return f"[Persona set to: {name}] (stub)"  # Hook to persona_manager
