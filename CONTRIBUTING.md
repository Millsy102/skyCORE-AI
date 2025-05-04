
# 🤝 Contributing to skyCORE-AI

We welcome contributions of all kinds — code, plugins, ideas, and documentation.

---

## 🧰 Setup Instructions

```bash
git clone https://github.com/your-username/skyCORE-AI.git
cd skyCORE-AI
pip install -r requirements.txt
python ui/main_window.py
```

---

## 🗂 Project Structure

| Folder           | Purpose                          |
|------------------|----------------------------------|
| `/src/`          | Core engine, memory, models, AI  |
| `/ui/`           | GUI layout (PySide6)             |
| `/plugins/`      | Installed plugin projects        |
| `/plugins_zips/` | Droppable plugin zips            |
| `/docs/`         | Developer + user documentation   |
| `.memory/`       | AI task logs, summaries          |

---

## 🧠 AI Development Tips

- Add new models to `model_manager.py`
- Add new slash commands in `slash_command_router.py`
- Log steps using `AgentLog` for traceability
- Use `.rules` for scoped AI behavior in your plugin

---

## 🚦 Workflow

1. Fork the repo
2. Create a branch: `feature/your-name`
3. Make changes
4. Open a Pull Request with a description

---

## 🙌 Thank you!

skyCORE-AI is community-powered and built to grow with devs like you. 💙
