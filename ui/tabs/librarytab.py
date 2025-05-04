
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QTextEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
import json
import os

class LibraryTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.snippet_list = QListWidget()
        self.snippet_list.itemClicked.connect(self.show_snippet)
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)

        self.import_btn = QPushButton("📥 Import JSON")
        self.export_btn = QPushButton("📤 Export All")
        self.save_btn = QPushButton("💾 Save New Snippet")

        self.import_btn.clicked.connect(self.import_snippets)
        self.export_btn.clicked.connect(self.export_snippets)
        self.save_btn.clicked.connect(self.save_snippet)

        btns = QHBoxLayout()
        btns.addWidget(self.import_btn)
        btns.addWidget(self.export_btn)
        btns.addWidget(self.save_btn)

        layout.addWidget(QLabel("📚 Prompt/Code Snippet Library"))
        layout.addWidget(self.snippet_list)
        layout.addLayout(btns)
        layout.addWidget(self.text_preview)
        self.setLayout(layout)

        self.path = os.path.join("memory", "snippets.json")
        os.makedirs("memory", exist_ok=True)
        self.snippets = {}
        self.load_snippets()

    def load_snippets(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.snippets = json.load(f)
        else:
            self.snippets = {"Hello": "Hello AI!", "Debug": "Trace the plugin runtime."}
        self.snippet_list.addItems(self.snippets.keys())

    def show_snippet(self, item):
        self.text_preview.setText(self.snippets[item.text()])

    def import_snippets(self):
        file, _ = QFileDialog.getOpenFileName(self, "Import Snippets", ".", "JSON (*.json)")
        if not file: return
        with open(file, "r") as f:
            data = json.load(f)
        self.snippets.update(data)
        self.snippet_list.clear()
        self.snippet_list.addItems(self.snippets.keys())

    def export_snippets(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export Snippets", "snippets.json", "JSON (*.json)")
        if not file: return
        with open(file, "w") as f:
            json.dump(self.snippets, f, indent=2)
        QMessageBox.information(self, "Exported", "📤 Snippets exported.")

    def save_snippet(self):
        name = "Snippet_" + str(len(self.snippets) + 1)
        self.snippets[name] = self.text_preview.toPlainText()
        self.snippet_list.addItem(name)
        with open(self.path, "w") as f:
            json.dump(self.snippets, f, indent=2)
