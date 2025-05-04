
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
import time

class ModelToolsTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)
        self.status = QTextEdit()
        self.status.setReadOnly(True)
        self.btn = QPushButton("🔍 Search HuggingFace Models")
        self.btn.clicked.connect(self.fetch_models)

        layout.addWidget(QLabel("🧠 HF Model Explorer"))
        layout.addWidget(self.btn)
        layout.addWidget(self.status)
        self.setLayout(layout)

    def fetch_models(self):
        self.status.setText("Searching...")
        time.sleep(1)
        models = ["gpt2", "mistral-7b-instruct", "bert", "phi-2", "starcoder"]
        self.status.setText("\n".join(f"🧠 {m}" for m in models))
