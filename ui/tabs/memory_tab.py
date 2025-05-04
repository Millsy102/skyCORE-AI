from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox
from src.memory_manager import MemoryManager
import json

class MemoryTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.runtime = runtime

        layout.addWidget(QLabel("🧠 Memory Viewer & Editor"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search memory...")
        self.search_input.textChanged.connect(self.search_memory)
        layout.addWidget(self.search_input)

        self.memory_view = QTextEdit()
        self.memory_view.setReadOnly(False)
        layout.addWidget(self.memory_view)

        self.save_btn = QPushButton("💾 Save Snapshot")
        self.save_btn.clicked.connect(self.save_snapshot)
        layout.addWidget(self.save_btn)

        self.load_btn = QPushButton("📂 Load .mem File")
        self.load_btn.clicked.connect(self.load_mem_file)
        layout.addWidget(self.load_btn)

        self.refresh_btn = QPushButton("🔄 Reload Memory")
        self.refresh_btn.clicked.connect(self.load_memory)
        layout.addWidget(self.refresh_btn)

        self.memory = MemoryManager()
        self.load_memory()

    def load_memory(self):
        summaries = self.memory.get_recent_summaries(50)
        self.raw_memory = summaries
        self.memory_view.setText("\n".join(summaries))

    def search_memory(self):
        query = self.search_input.text().lower()
        results = [m for m in self.raw_memory if query in m.lower()]
        self.memory_view.setText("\n".join(results))

    def save_snapshot(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Memory Snapshot", "memory_snapshot.mem", "Memory Files (*.mem)")
        if path:
            with open(path, "w") as f:
                json.dump(self.raw_memory, f)
            QMessageBox.information(self, "Saved", f"Snapshot saved to {path}")

    def load_mem_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Memory File", "", "Memory Files (*.mem)")
        if path:
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                    self.raw_memory = data
                    self.memory_view.setText("\n".join(data))
                    QMessageBox.information(self, "Loaded", f"Memory loaded from {path}")
                except:
                    QMessageBox.warning(self, "Invalid", "File is not a valid .mem format")
