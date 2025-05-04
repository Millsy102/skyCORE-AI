# 📦 Module imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from src.logger import log

# Class: PluginEditor — defines main behavior for plugin_editor.py
class PluginEditor(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QTextEdit()
        self.save_button = QPushButton("Save Plugin")
        self.save_button.clicked.connect(lambda: self.save_plugin)

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

# Function: load_plugin_code — handles a core step in this module
    def load_plugin_code(self, code=""):
        self.editor.setText(code)

# Function: save_plugin — handles a core step in this module
    def save_plugin(self):
        code = self.editor.toPlainText()
        try:
            with open("plugins/my_plugin/plugin.py", "w") as f:
                f.write(code)
            log("Plugin saved to plugins/my_plugin/plugin.py")
        except Exception as e:
            log(f"Failed to save plugin: {e}")