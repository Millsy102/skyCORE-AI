
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QTextEdit
from model_browser import HFModelBrowser

class ModelTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.browser = HFModelBrowser()

        layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.clicked.connect(self.search_models)
        search_layout.addWidget(QLabel("Search HuggingFace Models:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        # Model list
        self.model_list = QListWidget()
        self.model_list.itemClicked.connect(self.select_model)

        # Download + Switch + Info
        action_layout = QHBoxLayout()
        self.download_btn = QPushButton("📥 Download")
        self.download_btn.clicked.connect(self.download_model)
        self.switch_btn = QPushButton("🔁 Switch")
        self.switch_btn.clicked.connect(self.switch_model)
        self.test_btn = QPushButton("🧪 Test Prompt")
        self.test_btn.clicked.connect(self.test_prompt)
        action_layout.addWidget(self.download_btn)
        action_layout.addWidget(self.switch_btn)
        action_layout.addWidget(self.test_btn)

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addLayout(search_layout)
        layout.addWidget(self.model_list)
        layout.addLayout(action_layout)
        layout.addWidget(self.output)

    def search_models(self):
        query = self.search_input.text()
        self.model_list.clear()
        results = self.browser.search(query=query)
        self.model_list.addItems(results)

    def select_model(self, item):
        self.output.append(f"Selected: {item.text()}")

    def download_model(self):
        selected = self.model_list.currentItem()
        if selected:
            path = self.browser.download(selected.text())
            self.output.append(f"✅ Downloaded: {path}")

    def switch_model(self):
        selected = self.model_list.currentItem()
        if selected:
            model_id = selected.text()
            model, tokenizer = self.browser.use_model(model_id)
            self.runtime.ai_controller.set_model(model, tokenizer)
            self.output.append(f"🔁 Switched to: {model_id}")

    def test_prompt(self):
        selected = self.model_list.currentItem()
        if selected:
            prompt = "Hello AI, describe yourself."
            model, tokenizer = self.browser.use_model(selected.text())
            inputs = tokenizer(prompt, return_tensors="pt")
            output = model.generate(**inputs)
            decoded = tokenizer.decode(output[0], skip_special_tokens=True)
            self.output.append(f"🧪 Output: {decoded}")
