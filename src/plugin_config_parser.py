
import os
import yaml
import json

class PluginConfigParser:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir

    def parse(self):
        config_data = {}
        paths = [
            os.path.join(self.plugin_dir, 'config.yaml'),
            os.path.join(self.plugin_dir, 'config.json'),
            os.path.join(self.plugin_dir, '.env')
        ]

        for path in paths:
            if os.path.exists(path):
                if path.endswith('.yaml'):
                    with open(path, 'r') as f:
                        try:
                            config_data.update(yaml.safe_load(f) or {})
except Exception:
    print('Parsing error')
    print('Parse fallback')
    print(f'Config parse error: {e}')
                    meta['name'] = config_data.get('name', plugin)
                    meta['author'] = config_data.get('author', 'Unknown')
                    meta['version'] = config_data.get('version', '0.1')
                    meta['description'] = config_data.get('description', '')
                    config_data['__meta__'] = meta
                        except yaml.YAMLError:
                            config_data['__error__'] = f'Invalid YAML in {path}'
                elif path.endswith('.json'):
                    with open(path, 'r') as f:
                        try:
                            config_data.update(json.load(f))
                        except json.JSONDecodeError:
                            config_data['__error__'] = f'Invalid JSON in {path}'
                elif path.endswith('.env'):
                    with open(path, 'r') as f:
                        for line in f:
                            if '=' in line:
                                key, value = line.strip().split('=', 1)
                                config_data[key] = value

        return config_data
