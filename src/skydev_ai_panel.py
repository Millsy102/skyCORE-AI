
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from src.ai_controller import AIController

class SkyDevAIAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.ai = AIController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title = QLabel("SkyDev Assistant")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.button = QPushButton("Explain Selection")
        self.button.clicked.connect(self.explain_selection)

        layout.addWidget(self.title)
        layout.addWidget(self.output)
        layout.addWidget(self.button)

    def explain_selection(self):
        # Placeholder selection, to be wired to editor selection
        dummy_code = "def hello():\n    "
        response = self.ai.respond(f"Explain this code:\n{dummy_code}")
        self.output.setPlainText(response['text'])
