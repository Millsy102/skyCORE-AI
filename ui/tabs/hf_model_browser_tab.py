from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QComboBox, QHBoxLayout
import webbrowser
import requests
import os

class HFModelBrowserTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("🤖 HuggingFace Model Browser"))

        filter_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search HuggingFace models")
        filter_row.addWidget(self.search_input)

        self.tag_selector = QComboBox()
        self.tag_selector.addItems(["", "text-generation", "code", "vision", "conversational", "multilingual"])
        filter_row.addWidget(self.tag_selector)

        layout.addLayout(filter_row)

        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.clicked.connect(self.search)
        layout.addWidget(self.search_btn)

        self.results_view = QTextEdit()
        self.results_view.setReadOnly(True)
        layout.addWidget(self.results_view)

        self.download_btn = QPushButton("⬇️ Download Top Result")
        self.download_btn.clicked.connect(self.download_model)
        layout.addWidget(self.download_btn)

        self.link_btn = QPushButton("🌐 View on HuggingFace")
        self.link_btn.clicked.connect(self.open_in_browser)
        layout.addWidget(self.link_btn)

        self.last_model = None

    def search(self):
        term = self.search_input.text().strip()
        tag = self.tag_selector.currentText()
        try:
            url = f"https://huggingface.co/api/models?search={term}"
            r = requests.get(url)
            models = r.json()
            if tag:
                models = [m for m in models if tag in (m.get("tags") or [])]

            # Sort by downloads
            models.sort(key=lambda m: m.get("downloads", 0), reverse=True)

            display = []
            for m in models[:5]:
                safety = "✅" if m.get("verified") else "⚠️" if m.get("likes", 0) < 10 else "🟡"
                display.append(f"{safety} {m['modelId']} ({m.get('downloads', 0)} downloads)")
                display.append(f"📄 {m.get('description', '')[:100]}")
                display.append("")
            self.results_view.setText("\n".join(display))
            self.last_model = models[0]["modelId"] if models else None
        except Exception as e:
            self.results_view.setText(f"Error: {e}")

    def download_model(self):
        if not self.last_model:
            self.results_view.setText("No model selected.")
            return
        os.system(f"git clone https://huggingface.co/{self.last_model} models/{self.last_model}")
        self.results_view.append(f"✅ Downloaded {self.last_model}")
        # Registered to ModelRouter pipeline
        if hasattr(self.runtime, "model_router"):
            self.runtime.model_router.add(self.last_model)

    def open_in_browser(self):
        if self.last_model:
            webbrowser.open(f"https://huggingface.co/{self.last_model}")
