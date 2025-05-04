
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QTextEdit
import os
import json

class TraceViewerTab(QWidget):
    def __init__(self, memory_dir=".memory"):
        super().__init__()
        self.memory_dir = memory_dir
        self.layout = QVBoxLayout()
        self.list = QListWidget()
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.list.itemClicked.connect(self.load_log)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.output)
        self.setLayout(self.layout)
        self.refresh()

    def refresh(self):
        self.list.clear()
        if not os.path.isdir(self.memory_dir):
            return
        for f in sorted(os.listdir(self.memory_dir)):
            if f.startswith("console_") and f.endswith(".json"):
                self.list.addItem(f)

    def load_log(self, item):
        path = os.path.join(self.memory_dir, item.text())
        try:
            with open(path, "r") as f:
                data = json.load(f)
            self.output.setText(json.dumps(data, indent=2))
        except Exception as e:
            self.output.setText(f"Error loading: {e}")
