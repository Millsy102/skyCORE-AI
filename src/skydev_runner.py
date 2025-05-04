
import os
import subprocess

class PluginTestRunner:
    def __init__(self, plugins_path='plugins'):
        self.plugins_path = plugins_path

    def run(self):
        output = []
        for folder in os.listdir(self.plugins_path):
            plugin_dir = os.path.join(self.plugins_path, folder)
            test_file = os.path.join(plugin_dir, 'test.py')
            if not os.path.exists(test_file):
                continue

            output.append(f"== Running tests for {folder} ==")
            try:
                result = subprocess.run(['python', test_file], capture_output=True, text=True)
                output.append(result.stdout)
                if result.stderr:
                    output.append(f"[stderr]\n{result.stderr}")
            except Exception as e:
                output.append(f"Error running {test_file}: {e}")
        return "\n".join(output)
