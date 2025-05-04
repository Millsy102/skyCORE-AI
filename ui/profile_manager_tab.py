
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel
import os
import json

class ProfileManagerTab(QWidget):
    def __init__(self, profile_dir="profiles"):
        super().__init__()
        self.profile_dir = profile_dir
        self.layout = QVBoxLayout()
        self.label = QLabel("Select a profile to activate:")
        self.list = QListWidget()
        self.button = QPushButton("Activate Selected")
        self.button.clicked.connect(self.activate_selected)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.refresh()

    def refresh(self):
        self.list.clear()
        if not os.path.isdir(self.profile_dir):
            return
        for f in sorted(os.listdir(self.profile_dir)):
            if f.endswith(".skyprofile"):
                self.list.addItem(f)

    def activate_selected(self):
        selected = self.list.currentItem()
        if not selected:
            self.label.setText("⚠️ No profile selected")
            return

        path = os.path.join(self.profile_dir, selected.text())
        try:
            with open(path, "r") as f:
                data = json.load(f)
            os.environ.update({k: str(v) for k, v in data.items()})
            self.label.setText(f"✅ Activated: {selected.text()}")
        except Exception as e:
            self.label.setText(f"Error loading: {e}")
