
import os
import json
from datetime import datetime

class TraceLogger:
    def __init__(self, log_path='logs/trace_log.json'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def log(self, user_input, response):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'input': user_input,
            'response': response['text'],
            'tokens_used': response.get('tokens_used', 0),
            'model': response.get('model_used'),
            'plugins_triggered': response.get('plugins_triggered', []),
        }

        with open(self.log_path, 'r') as f:
            log_data = json.load(f)

        log_data.append(entry)

        with open(self.log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

    def get_log(self):
        with open(self.log_path, 'r') as f:
            return json.load(f)
