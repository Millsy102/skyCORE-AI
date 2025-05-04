# **skyCORE-AI Plugin System**

skyCORE-AI supports live, modular plugin loading — from `.zip` files or public GitHub repositories.

---

## **🧩 Plugin Basics**

Each plugin must include a `plugin.py` in its root folder, like:

```
class Plugin:
    def __init__(self):
        self.name = "ExamplePlugin"
        self.triggers = ["say hello", "run test"]

    def handle_input(self, query):
        return "Hello from plugin!"
```

---

## **⚙️ Plugin Features**

| Capability | How |
|------------|-----|
🧠 AI Routing | Triggered via AI chat using `self.triggers`  
🖥️ GUI Tabs | Include a `ui/*.py` QWidget and it will auto-load  
🎮 Subprocess UI | Add `gui_entry` to launch external PyQt/Tk/OBS GUI  
🧪 Lifecycle Hooks | Optional: `on_enable()`, `on_disable()`, `on_delete()`  
📁 Config Files | Stored under `config/plugin_name/` if needed  

---

## **🔌 Plugin Deployment**

- ✅ Drop `.zip` file into `plugins/`  
- ✅ Use **Plugin Installer** to paste a GitHub URL  
- 🔁 skyCORE-AI extracts, loads, and registers everything live

---

## **🧠 AI Intent Routing**

Plugins can react to:
- Exact triggers via `triggers = [...]`
- Partial or fuzzy match via `plugin_intent_router.py`
- Natural language fallback via `AI plugin mode`

---

## **🧰 Advanced Features**

| Feature | Description |
|--------|-------------|
📺 GUI sandbox | Plugins can use PyQt5/Tk via `gui_engine`  
🧠 Agent control | Plugins can route AI logic contextually  
☁️ Cloud sync | Plugins can store data in cloud config store  
🎥 OBS API | Plugins can switch scenes or sources  

---

## **🧼 Plugin Removal / Deactivation**

- Use `Plugins` tab to toggle or delete
- skyCORE-AI auto-reloads plugin index

---

For questions or plugin publishing, refer to `plugin_sdk.md` (TBD).