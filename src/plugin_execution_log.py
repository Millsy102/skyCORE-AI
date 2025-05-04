
import os
import json
from datetime import datetime

class PluginExecutionLog:
    def __init__(self, log_path='logs/plugin_exec_log.json'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def log(self, plugin, function, args, result):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'plugin': plugin,
            'function': function,
            'args': args,
            'result': result
        }

        with open(self.log_path, 'r') as f:
            logs = json.load(f)

        logs.append(entry)

        with open(self.log_path, 'w') as f:
            json.dump(logs, f, indent=2)

    def get_logs(self):
        with open(self.log_path, 'r') as f:
            return json.load(f)
