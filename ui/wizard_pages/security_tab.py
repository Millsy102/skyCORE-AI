# 📦 Module imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox

# Class: SecurityTab — defines main behavior for security_tab.py
class SecurityTab(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.settings = runtime.settings

        layout = QVBoxLayout(self)

        self.nsfw = QCheckBox("Allow NSFW content")
        self.nsfw.setChecked(self.settings.get("nsfw_allowed", False))

        self.telemetry = QCheckBox("Enable anonymous telemetry")
        self.telemetry.setChecked(self.settings.get("telemetry", False))

        self.sandbox = QCheckBox("Restrict plugins (Sandbox Mode)")
        self.sandbox.setChecked(self.settings.get("plugin_sandbox", True))

        self.logging_level = QComboBox()
        self.logging_level.addItems(["info", "warning", "error", "debug"])
        self.logging_level.setCurrentText(self.settings.get("logging_level", "info"))

        layout.addWidget(QLabel("🔐 Privacy & Security Settings"))
        layout.addWidget(self.nsfw)
        layout.addWidget(self.telemetry)
        layout.addWidget(self.sandbox)
        layout.addWidget(QLabel("📋 Logging Level"))
        layout.addWidget(self.logging_level)

# Function: save — handles a core step in this module
    def save(self):
        self.settings.set("nsfw_allowed", self.nsfw.isChecked())
        self.settings.set("telemetry", self.telemetry.isChecked())
        self.settings.set("plugin_sandbox", self.sandbox.isChecked())
        self.settings.set("logging_level", self.logging_level.currentText())
