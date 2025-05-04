import importlib.util, os

def test_plugin(path):
    entry = os.path.join(path, "main.py")
    if not os.path.exists(entry): return print("❌ No main.py")
    spec = importlib.util.spec_from_file_location("main", entry)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        if hasattr(mod, "run"): mod.run()
        else: print("⚠️ No run() method")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_plugin(input("Plugin path: "))
