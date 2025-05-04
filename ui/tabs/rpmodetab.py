
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QTextEdit

class RPModeTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.modes = {
            "Romantic": "You are gentle, caring, and emotionally expressive.",
            "Friendly": "You are upbeat, cheerful, and humorous.",
            "Dominant": "You are assertive, confident, and slightly teasing.",
            "Submissive": "You are shy, gentle, and eager to please.",
            "Narrative": "You respond with rich, detailed storytelling.",
            "Custom": ""
        }
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(self.modes.keys())
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.apply_btn = QPushButton("🎭 Apply Mode")
        self.apply_btn.clicked.connect(self.apply_mode)

        layout.addWidget(QLabel("🎭 Choose Roleplay Style:"))
        layout.addWidget(self.mode_selector)
        layout.addWidget(self.preview)
        layout.addWidget(self.apply_btn)
        self.setLayout(layout)
        self.update_preview()

        self.mode_selector.currentTextChanged.connect(self.update_preview)

    def update_preview(self):
        mode = self.mode_selector.currentText()
        self.preview.setText(self.modes.get(mode, ""))

    def apply_mode(self):
        mode = self.mode_selector.currentText()
        self.runtime.settings.set("rp_mode", mode)
        QMessageBox.information(self, "RP Mode", f"🎭 Mode '{mode}' applied.")
