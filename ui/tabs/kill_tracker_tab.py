from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
import subprocess
import os

class KillTrackerTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("🎮 Kill Tracker Launcher"))

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        launch_btn = QPushButton("▶️ Launch Tracker")
        launch_btn.clicked.connect(self.launch_tool)
        layout.addWidget(launch_btn)

    def launch_tool(self):
        try:
            subprocess.Popen(["python", "external/SCTool-Tracker-Git/Kill_main.py"])
            self.console.append("✅ Tracker Launched.")
        except Exception as e:
            self.console.append(f"❌ {e}")
