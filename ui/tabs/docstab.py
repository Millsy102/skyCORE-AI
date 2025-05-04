
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog
import os

class DocsTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.export_btn = QPushButton("📤 Export to TXT")
        self.export_btn.clicked.connect(self.export)

        layout.addWidget(QLabel("📄 Plugin Documentation"))
        layout.addWidget(self.output)
        layout.addWidget(self.export_btn)
        self.setLayout(layout)
        self.generate_docs()

    def generate_docs(self):
        docs = []
        for name, plugin in self.runtime.plugin_loader.plugins.items():
            desc = plugin.get("description", "No description")
            triggers = plugin.get("triggers", [])
            docs.append(f"📦 {name}\n📝 {desc}\n🔫 Triggers: {', '.join(triggers)}")
        self.output.setText("\n\n".join(docs))

    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Docs", "plugin_docs.txt", "Text Files (*.txt)")
        if path:
            with open(path, "w") as f:
                f.write(self.output.toPlainText())
