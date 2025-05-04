# **🧑‍💻 Developer Guide – SkyCORE SDK**

Welcome to SkyCORE SDK!

## **🔨 Building a Plugin**

Each plugin lives in its own folder under `plugins/`.

### **Plugin Structure:**
```
my_plugin/
├── plugin.py
├── meta.json
└── plugin_ui_panel.js  # optional GUI tab
```

### **`plugin.py` entrypoints:**
- `run()` – required main logic
- `describe()` – AI summary
- Optional: signal listeners (`on_plugin_run`)

## **🧪 Testing Tools**
Use:
- `tools/plugin_tester.py`
- `tools/patch_builder.py`
- SDK auto-tab injection

## **💡 Tips:**
- Include `plugin_ui_panel.js` to auto-tab
- Provide `meta.json` for marketplace submission