# 📦 Module imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox

# Class: ApiTab — defines main behavior for api_tab.py
class ApiTab(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.settings = runtime.settings

        layout = QVBoxLayout(self)

        self.openai = QLineEdit()
        self.openai.setPlaceholderText("OpenAI API Key")
        self.openai.setEchoMode(QLineEdit.Password)

        self.hf = QLineEdit()
        self.hf.setPlaceholderText("HuggingFace Token")
        self.hf.setEchoMode(QLineEdit.Password)

        self.anthropic = QLineEdit()
        self.anthropic.setPlaceholderText("Anthropic API Key")
        self.anthropic.setEchoMode(QLineEdit.Password)

        self.show_toggle = QCheckBox("Show API Keys")
        self.show_toggle.stateChanged.connect(self.toggle_visibility)

        layout.addWidget(QLabel("🔐 OpenAI Key"))
        layout.addWidget(self.openai)
        layout.addWidget(QLabel("🤗 HuggingFace Key"))
        layout.addWidget(self.hf)
        layout.addWidget(QLabel("🧠 Anthropic Key"))
        layout.addWidget(self.anthropic)
        layout.addWidget(self.show_toggle)

# Function: toggle_visibility — handles a core step in this module
    def toggle_visibility(self, state):
        mode = QLineEdit.Normal if state else QLineEdit.Password
        self.openai.setEchoMode(mode)
        self.hf.setEchoMode(mode)
        self.anthropic.setEchoMode(mode)

# Function: save — handles a core step in this module
    def save(self):
        self.settings.set("openai_api_key", self.openai.text())
        self.settings.set("hf_api_key", self.hf.text())
        self.settings.set("anthropic_api_key", self.anthropic.text())
