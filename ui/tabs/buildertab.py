
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
import os
import json

class BuilderTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.name_input = QLineEdit()
        self.create_btn = QPushButton("🚀 Generate Plugin")
        self.create_btn.clicked.connect(self.build)

        layout.addWidget(QLabel("📦 New Plugin Name"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.create_btn)
        self.setLayout(layout)

    def build(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing", "⚠️ Enter a valid name.")
            return
        path = os.path.join("plugins", name)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "main.py"), "w") as f:
            f.write("def register(self, *args, **kwargs):
        return f"🔧 register executed with args={args} kwargs={kwargs}"")
        with open(os.path.join(path, "manifest.json"), "w") as f:
            json.dump({"name": name, "version": "0.1", "triggers": [name]}, f, indent=2)
        QMessageBox.information(self, "Created", f"✅ Plugin '{name}' created.")
