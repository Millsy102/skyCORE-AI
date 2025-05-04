from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, QFileDialog, QMessageBox
from src.persona_manager import PersonaManager
import json

class PersonaTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.runtime = runtime
        self.persona = PersonaManager()

        layout.addWidget(QLabel("👤 Active Persona"))

        self.label = QLabel(self.persona.get_active())
        layout.addWidget(self.label)

        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Persona Notes / Role Description")
        layout.addWidget(self.notes)

        self.traits = QLineEdit()
        self.traits.setPlaceholderText("Comma-separated traits (e.g. creative, concise)")
        layout.addWidget(self.traits)

        btn_set = QPushButton("Activate")
        btn_set.clicked.connect(self.activate)
        layout.addWidget(btn_set)

        btn_save = QPushButton("💾 Save Persona")
        btn_save.clicked.connect(self.save_persona)
        layout.addWidget(btn_save)

        btn_load = QPushButton("📂 Load Persona")
        btn_load.clicked.connect(self.load_persona)
        layout.addWidget(btn_load)

    def activate(self):
        traits = self.traits.text().split(",")
        desc = self.notes.toPlainText()
        name = "custom"
        self.persona.set(name, {"description": desc, "traits": traits})
        self.persona.set_active(name)
        self.label.setText(name)

    def save_persona(self):
        data = {
            "description": self.notes.toPlainText(),
            "traits": self.traits.text().split(",")
        }
        path, _ = QFileDialog.getSaveFileName(self, "Save Persona", "persona.json", "JSON (*.json)")
        if path:
            with open(path, "w") as f:
                json.dump(data, f)
            QMessageBox.information(self, "Saved", f"Persona saved to {path}")

    def load_persona(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Persona", "", "JSON (*.json)")
        if path:
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                self.notes.setText(data.get("description", ""))
                self.traits.setText(",".join(data.get("traits", [])))
            except:
                QMessageBox.warning(self, "Load Failed", "Invalid persona file")
