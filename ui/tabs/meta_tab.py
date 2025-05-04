# 📦 Module imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QApplication
from PySide6.QtCore import QDateTime
import platform
import psutil
import clipboard

# Class: MetaTab — defines main behavior for meta_tab.py
class MetaTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.layout = QVBoxLayout(self)

        self.labels = []

        self.refresh_btn = QPushButton("🔄 Refresh Stats")
        self.copy_btn = QPushButton("📋 Copy to Clipboard")
        self.refresh_btn.clicked.connect(self.refresh_stats)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        self.layout.addWidget(QLabel("📊 System Diagnostics"))
        self.layout.addWidget(self.refresh_btn)
        self.layout.addWidget(self.copy_btn)

        self.refresh_stats()
        self.setLayout(self.layout)

    def refresh_stats(self):
        # Clear previous labels
        for lbl in self.labels:
            self.layout.removeWidget(lbl)
            lbl.deleteLater()
        self.labels.clear()

        # Update system stats
        model_name = self.runtime.settings.get("default_model", "Unknown")
        persona_name = self.runtime.persona.get_current()
        plugin_count = len(self.runtime.plugin_loader.plugins)
        mem_used = psutil.virtual_memory().used // (1024 * 1024)
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")

        stats = [
            f"📅 Timestamp: {timestamp}",
            f"🧬 Python Version: {platform.python_version()}",
            f"🧠 Active Model: {model_name}",
            f"🎭 Current Persona: {persona_name}",
            f"🔌 Plugins Loaded: {plugin_count}",
            f"🧠 Runtime Memory (MB): {mem_used}",
            f"📦 SkyCore Runtime Objects: {len(dir(self.runtime))}"
        ]

        for stat in stats:
            lbl = QLabel(stat)
            self.layout.addWidget(lbl)
            self.labels.append(lbl)

    def copy_to_clipboard(self):
        data = "\n".join(label.text() for label in self.labels)
        clipboard.copy(data)
        QMessageBox.information(self, "Copied", "📋 System info copied to clipboard.")
