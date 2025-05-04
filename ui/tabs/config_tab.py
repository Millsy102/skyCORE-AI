from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QFileDialog, QMessageBox
import os

class ConfigTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("🛠 Core Config Files Editor"))

        self.config_selector = QComboBox()
        self.config_files = [f for f in os.listdir("config") if f.endswith((".json", ".yaml", ".yml"))]
        self.config_selector.addItems(self.config_files)
        self.config_selector.currentTextChanged.connect(self.load_config)
        layout.addWidget(self.config_selector)

        self.editor = QTextEdit()
        layout.addWidget(self.editor)

        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)

        self.load_config()

    def load_config(self):
        filename = self.config_selector.currentText()
        path = os.path.join("config", filename)
        if os.path.exists(path):
            with open(path, "r") as f:
                self.editor.setText(f.read())

    def save_config(self):
        filename = self.config_selector.currentText()
        path = os.path.join("config", filename)
        with open(path, "w") as f:
            f.write(self.editor.toPlainText())
        QMessageBox.information(self, "Saved", f"{filename} saved.")
