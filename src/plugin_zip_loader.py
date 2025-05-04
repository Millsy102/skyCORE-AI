
import os
import zipfile

class PluginZipLoader:
    def __init__(self, zip_dir='plugins_zips', extract_dir='plugins'):
        self.zip_dir = zip_dir
        self.extract_dir = extract_dir
        os.makedirs(self.zip_dir, exist_ok=True)
        os.makedirs(self.extract_dir, exist_ok=True)

    def extract_all(self):
        results = []
        for file in os.listdir(self.zip_dir):
            if file.endswith('.zip'):
                zip_path = os.path.join(self.zip_dir, file)
                plugin_name = file.replace('.zip', '')
                extract_path = os.path.join(self.extract_dir, plugin_name)

                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                    results.append(f"✔ Extracted {file} to {extract_path}")
                except Exception as e:
                    results.append(f"✖ Failed to extract {file}: {e}")

        return "\n".join(results)
