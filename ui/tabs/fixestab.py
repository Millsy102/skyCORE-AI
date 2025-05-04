
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
import os

class FixesTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.output = QTextEdit()
        self.repair_btn = QPushButton("🔧 Auto-Fix Core Dirs")
        self.repair_btn.clicked.connect(self.repair)
        layout.addWidget(self.repair_btn)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def repair(self):
        log = []
        for folder in ["plugins", "memory", "logs", "themes"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                log.append(f"📁 Created: {folder}")
        self.output.setText("\n".join(log) or "✔️ All core folders OK")
