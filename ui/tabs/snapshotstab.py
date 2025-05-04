
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QListWidget
import json
import os
import time

class SnapshotsTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.snapshot_list = QListWidget()
        self.refresh_btn = QPushButton("🔁 Refresh")
        self.load_btn = QPushButton("📂 Load Selected")
        self.save_btn = QPushButton("💾 Save New Snapshot")

        layout.addWidget(QLabel("📸 Saved Snapshots"))
        layout.addWidget(self.snapshot_list)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

        self.refresh_btn.clicked.connect(self.refresh_list)
        self.load_btn.clicked.connect(self.load_selected)
        self.save_btn.clicked.connect(self.save_snapshot)

        self.dir = "memory/snapshots"
        os.makedirs(self.dir, exist_ok=True)
        self.refresh_list()

    def refresh_list(self):
        self.snapshot_list.clear()
        if not os.path.exists(self.dir):
            return
        for file in os.listdir(self.dir):
            if file.endswith(".json"):
                self.snapshot_list.addItem(file)

    def save_snapshot(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = os.path.join(self.dir, f"snapshot_{timestamp}.json")
        data = {
            "settings": self.runtime.settings.to_dict(),
            "persona": self.runtime.persona.export_all(),
            "memory": self.runtime.memory.export(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        QMessageBox.information(self, "Saved", f"✅ Snapshot saved as {os.path.basename(path)}")
        self.refresh_list()

    def load_selected(self):
        selected = self.snapshot_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Load Error", "⚠️ No snapshot selected.")
            return
        path = os.path.join(self.dir, selected.text())
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.runtime.settings.load_from_dict(data.get("settings", {}))
        self.runtime.persona.import_all(data.get("persona", {}))
        self.runtime.memory.import_data(data.get("memory", []))
        QMessageBox.information(self, "Loaded", "✅ Snapshot applied.")
