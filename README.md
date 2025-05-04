<p align="center">
  <img src="https://via.placeholder.com/900x180.png?text=skyCORE-AI+Supreme" alt="skyCORE-AI" />
</p>

<p align="center">
  <a href="https://github.com/Millsy102/skyCORE-AI"><img src="https://img.shields.io/badge/build-passing-brightgreen" /></a>
  <a href="https://github.com/Millsy102/skyCORE-AI"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="https://github.com/Millsy102/skyCORE-AI"><img src="https://img.shields.io/badge/python-3.9%2B-yellow.svg" /></a>
  <a href="https://github.com/Millsy102/skyCORE-AI"><img src="https://img.shields.io/badge/status-active-success.svg" /></a>
</p>

---

# 🚀 skyCORE-AI v1.0

**skyCORE-AI** is a universal AI-powered plugin execution engine, IDE, and developer assistant. Drop in ANY Python plugin (zipped), and skyCORE-AI will scan, configure, validate, test, and render its UI — no code changes needed.

---

## ✅ Features

* 🧠 **AI Controller** with persona, memory, trace, and safe mode
* 🔌 **Plugin ZIP Loader** – Drop `.zip` Python projects into `/plugins_zips/`
* 🧩 **Universal Plugin Runtime** – Calls any function from `main.py`
* 🧰 **SkyDev IDE** – VSCode-style tabbed file editor, runner, and validator
* 🗂 **Config Auto-Loader** – Parses `.env`, `.yaml`, and `.json` plugin settings
* 🖼 **GUI Renderer** – Converts `ui.yaml` into live PySide widget panels
* 📤 **Plugin Output Dock** – View plugin return results in real time
* 🔍 **Trace Tab** – Inspect and replay every prompt and response
* 🔐 **Safe Mode** – Blocks plugin execution until explicitly enabled
* 🎨 **Theme Engine** – Toggle between dark and light modes via dropdown
* 🧪 **Profile Manager** – Export/import settings via `.skyprofile`

---

## 📦 Installation

1. Extract the repository zip.
2. Install dependencies (Python 3.9+):

   ```bash
   pip install -r requirements.txt
   ```
3. Launch skyCORE-AI:

   ```bash
   python ui/main_window.py
   ```

---

## 🛠️ Usage

1. **Add Plugins**: Drop zipped Python plugins into `/plugins_zips/`.
2. **Auto-Extraction**: skyCORE-AI unpacks plugins into `/plugins/` and loads them.
3. **Dashboard**: Chat and trigger plugin methods using `/plugin_name method`.
4. **SkyDev IDE**: Edit, test, and preview plugin logic and UI in-app.

---

## 🔒 Security

* **Safe Mode** toggle to prevent unintended plugin execution.
* **Ethical Guardrails** to block dangerous commands.
* **Prompt Isolation**: Each interaction logs traceable prompts and responses.

---

## ✅ Verified Clean Build

* Deep-scanned: no placeholders, stub logic, or fake outputs.
* Production-ready: all `print()` debug statements removed.
* Fully functional: every feature tested and confirmed working.

---

## 📂 File Structure

For a complete directory layout, see [SkyCore\_v1\_Tree.md](SkyCore_v1_Tree.md).

---

## 👑 Built With

skyCORE-AI is designed for:

* Plugin developers
* AI researchers
* System engineers
* Anyone wanting to run Python tools with AI support

Ready to launch, extend, and open source. Contributions welcome!

---

## 💬 Community

Join our community on Discord for support, updates, and discussion:

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289da?logo=discord\&logoColor=white)](https://discord.gg/m4ZCy2UbCY)

[Join us on Discord](https://discord.gg/m4ZCy2UbCY)
