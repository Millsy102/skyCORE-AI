from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from src.profile_manager import ProfileManager

class ProfileTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.pm = ProfileManager()

        layout.addWidget(QLabel("👥 Profile Manager"))

        self.current = QLabel(f"Active: {self.pm.get('active') or 'None'}")
        layout.addWidget(self.current)

        self.input = QLineEdit()
        self.input.setPlaceholderText("New profile name")
        layout.addWidget(self.input)

        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Notes for this profile")
        layout.addWidget(self.notes)

        switch_btn = QPushButton("Activate Profile")
        switch_btn.clicked.connect(self.switch_profile)
        layout.addWidget(switch_btn)

    def switch_profile(self):
        name = self.input.text()
        self.pm.set("active", name)
        self.pm.set("notes", self.notes.toPlainText())
        self.current.setText(f"Active: {name}")
