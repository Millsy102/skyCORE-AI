# 🌐 skyCORE-AI

> ⚠️ **Status:** Currently in final bug-fixing phase — feature updates are coming soon. 📦 Screenshots coming soon!

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/build-passing-brightgreen"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.9%2B-yellow.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/status-stable-lightgrey"></a>
  <a href="https://discord.gg/m4ZCy2UbCY"><img src="https://img.shields.io/discord/1219648107884443648?label=Join%20Discord&logo=discord&style=flat&color=5865F2"></a>
</p>

---

## 🚀 What is skyCORE-AI?

**skyCORE-AI** is an advanced, AI-powered plugin engine and developer platform. It lets you drop in zipped Python plugins, chat with models like GPT-4 or Claude, edit code in a built-in IDE, and manage plugin lifecycles — all in one sleek interface.

Whether you're building tools, testing AI logic, or running modular automations — **skyCORE-AI gives you a cockpit for everything Python.**

---

## ✨ Core Features

* 🔌 **Drop-in Plugin Loader** — Auto-installs Python `.zip` plugins via `/plugins_zips/`
* 🧠 **AI Model Control** — Route prompts to GPT-4, Claude, Hugging Face, or local models
* 🛠 **SkyDev IDE** — Code editor with tabs, preview, test runner, and YAML UI renderer
* 🧩 **Plugin Reflection** — Parses `main.py`, loads metadata, reads `ui.yaml` for GUI
* 💬 **AI Chat Dashboard** — Use slash commands to code, call plugins, or edit files
* 🔁 **Trace Tab** — Record and replay prompt/plugin execution
* 🔐 **Safe Mode** — Block plugin execution until explicitly enabled
* 💾 **Profile System** — Save/load user state and model settings via `.skyprofile`

---

## 📦 Installation

```bash
git clone https://github.com/Millsy102/skyCORE-AI.git
cd skyCORE-AI
pip install -r requirements.txt  # or: pip install PySide6
python ui/main_window.py
```

---

### 🪟 Windows Quick Launch (Optional)

If you're on Windows, you can use the included `launch_skycore.bat` file for quick startup:

```bat
@echo off
cd /d %~dp0
python ui/main_window.py
```

Just double-click the `.bat` file to launch skyCORE-AI.

> 💡 **Note:** Make sure `python` is added to your system PATH for this to work.

---

## 🧠 AI Dev Commands

Use slash commands inside the Dashboard:

* `/model claude` — switch models
* `/file edit path.py fix indentation` — AI rewrites the file
* `/plugin demo run` — execute plugin function
* `Generate a plugin that converts Markdown to PDF` — AI scaffolds code

---

## 📁 Plugin Project Format

```
myplugin/
├── main.py         # logic entrypoint
├── config.yaml     # plugin metadata
├── ui.yaml         # optional GUI layout
└── test.py         # optional tests
```

To use:

* Zip your plugin folder
* Drop it in `/plugins_zips/`
* skyCORE-AI does the rest

---

## 📂 Folder Overview

| Folder           | Purpose                               |
| ---------------- | ------------------------------------- |
| `/plugins/`      | Installed plugin projects             |
| `/plugins_zips/` | Drop zipped plugin folders here       |
| `/profiles/`     | Saved configuration snapshots         |
| `/ui/`           | GUI and tab layouts                   |
| `/src/`          | AI backend, plugin engine, core logic |

---

## 📃 License

skyCORE-AI is released under the **MIT License** — free to use, share, and modify. Contributions welcome.

---

## 🙌 Credits

* Built and designed by [@Millsy102](https://github.com/Millsy102)
* Developed with help from ChatGPT
* Powered by: Python, PySide6, OpenAI, Hugging Face, and ✨ you
