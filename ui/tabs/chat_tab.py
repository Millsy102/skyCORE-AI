from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox
from src.model_router import ModelRouter
from src.persona_manager import PersonaManager
from src.plugin_loader import PluginLoader
from src.agent_router import AgentRouter

class ChatTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        # Row: Model and Persona dropdowns
        switch_row = QHBoxLayout()
        self.model_selector = QComboBox()
        self.model_selector.addItems(["gpt-4", "local/llama", "hf/mistral"])
        self.model_selector.currentTextChanged.connect(self.switch_model)
        switch_row.addWidget(QLabel("Model:"))
        switch_row.addWidget(self.model_selector)

        self.persona_selector = QComboBox()
        self.persona_selector.addItems(["default", "dev", "debug", "tester"])
        self.persona_selector.currentTextChanged.connect(self.switch_persona)
        switch_row.addWidget(QLabel("Persona:"))
        switch_row.addWidget(self.persona_selector)

        layout.addLayout(switch_row)

        # Prompt input
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask or instruct...")
        layout.addWidget(self.input_box)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.run_chat)
        layout.addWidget(self.send_btn)

        # Output panel (markdown/text)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Analyzer preview
        self.preview_label = QLabel("🔍 Classifier: N/A | Plugin: N/A | Est. Cost: $0.00")
        layout.addWidget(self.preview_label)

        # Models
        self.model_router = ModelRouter()
        self.persona_manager = PersonaManager()
        self.plugins = PluginLoader().plugins
        self.classifier = AgentRouter()

    def switch_model(self, name):
        self.model_router.set_active(name)

    def switch_persona(self, persona):
        self.persona_manager.set_active(persona)

    def run_chat(self):
        prompt = self.input_box.text()
        class_type = self.classifier.classify(prompt)
        plugin_detected = next((p for p in self.plugins if p in prompt.lower()), "None")
        cost = round(len(prompt) * 0.00001, 5)

        self.preview_label.setText(f"🔍 Classifier: {class_type} | Plugin: {plugin_detected} | Est. Cost: ${cost}")
        response = f"{prompt[::-1]}"

        response = prompt[::-1]

    def switch_agent(self, name):
        self.agent_input.setText(name)
        self.console.append(f"🧠 Agent switched to: {name}")
    