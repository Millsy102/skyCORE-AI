import os, yaml

def lint_plugin(path):
    errors = []
    if not os.path.exists(f"{path}/main.py"):
        errors.append("❌ Missing main.py")
    if os.path.exists(f"{path}/config.yaml"):
        try: yaml.safe_load(open(f"{path}/config.yaml"))
        except: errors.append("❌ Invalid config.yaml")
    else:
        errors.append("❌ Missing config.yaml")
    print("\n".join(errors) if errors else "✅ Passed")

if __name__ == "__main__":
    p = input("Path to plugin: ")
    lint_plugin(p)
