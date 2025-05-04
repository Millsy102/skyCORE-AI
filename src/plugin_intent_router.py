import os
import importlib.util

class PluginIntentRouter:
    def __init__(self, plugin_root="plugins"):
        self.plugin_root = plugin_root
        self.plugin_map = self._scan_plugins()

    def _scan_plugins(self):
        trigger_map = {}
        for plugin_name in os.listdir(self.plugin_root):
            plugin_file = os.path.join(self.plugin_root, plugin_name, "plugin.py")
            if not os.path.exists(plugin_file):
                continue

            spec = importlib.util.spec_from_file_location(f"{plugin_name}.plugin", plugin_file)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                if hasattr(mod, "Plugin"):
                    plugin_instance = mod.Plugin()
                    if hasattr(plugin_instance, "triggers"):
                        for trig in plugin_instance.triggers:
                            trigger_map[trig.lower()] = plugin_instance
            except Exception as e:
    print('Intent route error')

    def route(self, input_string):
        for trigger, plugin in self.plugin_map.items():
            if trigger in input_string.lower():
                return plugin.execute({"input": input_string})
        

        # OBS Command Injection
        if "start stream" in input_string.lower():
            from src.obs_controller import OBSController
        obs = OBSController(password=os.getenv('OBS_PASSWORD', 'default'))
            obs.connect()
            return {"response": obs.start_streaming()}
        if "stop stream" in input_string.lower():
            from src.obs_controller import OBSController
        obs = OBSController(password=os.getenv('OBS_PASSWORD', 'default'))
            obs.connect()
            return {"response": obs.stop_streaming()}
        if "switch scene to" in input_string.lower():
            import re
            match = re.search(r"switch scene to (.+)", input_string.lower())
            if match:
                scene = match.group(1).strip().title()
                from src.obs_controller import OBSController
        obs = OBSController(password=os.getenv('OBS_PASSWORD', 'default'))
                obs.connect()
                return {"response": obs.change_scene(scene)}

        return {"response": "🤖 No matching plugin found for input."}
