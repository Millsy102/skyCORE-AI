import os, yaml

def create_plugin(name):
    base = f"plugins/{name}"
    os.makedirs(base, exist_ok=True)
    with open(f"{base}/main.py", "w") as f:
        f.write(f"def run():\n    print('{name} plugin running')\n")
    with open(f"{base}/config.yaml", "w") as f:
        yaml.dump({"name": name, "version": "1.0", "author": "you"}, f)
    with open(f"{base}/ui.yaml", "w") as f:
        f.write("layout: vertical\nfields:\n  - name: input\n    type: text")
    print(f"✅ Plugin '{name}' created.")

if __name__ == "__main__":
    plugin_name = input("Plugin name: ")
    create_plugin(plugin_name)
