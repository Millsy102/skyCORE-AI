<p align="center">
  <img src="https://via.placeholder.com/900x180.png?text=skyCORE-AI+Supreme" alt="skyCORE-AI" />
</p>

<p align="center">
  <a href="https://github.com/Millsy102/skyCORE-AI/actions"><img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status" /></a>
  <a href="https://github.com/Millsy102/skyCORE-AI/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" /></a>
  <a href="https://github.com/Millsy102/skyCORE-AI"><img src="https://img.shields.io/badge/python-3.9%2B-yellow.svg" alt="Python Version" /></a>
  <a href="https://discord.gg/m4ZCy2UbCY"><img src="https://img.shields.io/badge/discord-community-5865F2?logo=discord&logoColor=white" alt="Discord Community" /></a>
</p>

---

# 🚀 skyCORE-AI v1.0

An open-source, OS-like platform and plugin execution engine with AI-driven automation and a multi-tab interface. Drop any zipped Python plugin into `/plugins_zips/`, and skyCORE-AI will auto-scan, configure, validate, test, and render its UI—no code changes required.

## 📋 Table of Contents1. [Key Features](#-key-features)

2. [Prerequisites](#-prerequisites)

* Python 3.9 or higher
* `pip` package manager
* Optional: Virtual environment tool (venv, pyenv, Poetry)

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/Millsy102/skyCORE-AI.git
cd skyCORE-AI

# (Optional) create and activate virtual environment
python -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Quick Start

1. **Launch the app**:

   ```bash
   python ui/main_window.py
   ```
2. **Add plugins**: Place your zipped Python plugin (with `main.py` and optional `ui.yaml`) into `/plugins_zips/`.
3. **Trigger plugin**: In Dashboard chat input, type:

   ```text
   /<plugin_name> <function_name> arg1=value1 arg2=value2
   ```
4. **Develop**: Switch to SkyDev IDE tab to edit, test, and live-preview UI components.

---

## 🛠️ Plugin Development Guide

1. **Structure**:

   ```plaintext
   my_plugin.zip
   ├── main.py      # Exports functions to be called
   ├── requirements.txt  # Plugin-specific deps
   └── ui.yaml      # (Optional) UI layout definitions
   ```
2. **main.py**:

   ```python
   ```

def hello(name: str) -> str:
return f"Hello, {name}!"

````
3. **ui.yaml** example:
```yaml
window:
  title: "Hello Plugin"
  widgets:
    - type: TextInput
      id: name_input
      label: "Name"
    - type: Button
      id: hello_btn
      label: "Say Hello"
      action: "hello(name=name_input.value)"
````

4. **Load**: Drop `my_plugin.zip` into `/plugins_zips/`, then open Dashboard to call `/my_plugin hello name=World`.

---

## 🔧 Configuration

Create or update `.env`, `.config.yaml`, or `.config.json` in plugin root to set custom parameters. Variables are auto-loaded into the plugin namespace.

---

## 📟 CLI Usage

skyCORE-AI also provides a command-line interface:

```bash
# List available plugins
skycore list

# Invoke plugin function
skycore run my_plugin hello --name World

# Export profile
skycore profile export --output default.skyprofile
```

Use `skycore --help` for full command reference.

---

## 📂 File Structure

```plaintext
skyCORE-AI/
├── plugins_zips/         # Drop zipped plugins here
├── plugins/              # Auto-extracted plugin folders
├── ui/                   # Application UI source (PySide6)
│   └── main_window.py    # Entry point
├── skycore/              # Core engine modules
├── tests/                # Unit and integration tests
├── requirements.txt      # Global dependencies
├── SkyCore_v1_Tree.md    # Detailed directory layout
├── .gitignore
└── LICENSE
```

---

## 👑 Built With

* **Python 3.9+**
* **PySide6** for desktop UI
* **OpenAI GPT** (via API) for AI controller
* **Click** for CLI commands
* **PyYAML** for configuration parsing

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit and push your changes
4. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details and coding guidelines.

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 💬 Community & Support

Join our Discord for real-time help, announcements, and collaboration:

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289da?logo=discord\&logoColor=white)](https://discord.gg/m4ZCy2UbCY)

Questions? Open an issue or start a discussion on GitHub.
