# 📦 Module imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox

# Class: GeneralTab — defines main behavior for general_tab.py
class GeneralTab(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.settings = runtime.settings

        layout = QVBoxLayout(self)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Your name or alias")

        self.theme = QComboBox()
        self.theme.addItems(["Dark", "Light", "Matrix", "Classic"])

        self.memory_toggle = QCheckBox("Enable session memory")
        self.memory_toggle.setChecked(True)

        layout.addWidget(QLabel("👤 Username"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("🎨 Theme"))
        layout.addWidget(self.theme)
        layout.addWidget(self.memory_toggle)

# Function: save — handles a core step in this module
    def save(self):
        self.settings.set("username", self.username.text())
        self.settings.set("theme", self.theme.currentText())
        self.settings.set("enable_memory", self.memory_toggle.isChecked())
