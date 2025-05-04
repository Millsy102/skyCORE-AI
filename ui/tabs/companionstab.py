
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox

class CompanionsTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.companion_list = QListWidget()
        self.details = QLabel("🧠 Select a companion to view details.")
        self.activate_btn = QPushButton("🤖 Activate Companion")
        self.activate_btn.clicked.connect(self.activate)

        layout.addWidget(QLabel("🤖 Companion AI Directory"))
        layout.addWidget(self.companion_list)
        layout.addWidget(self.details)
        layout.addWidget(self.activate_btn)
        self.setLayout(layout)

        self.load_companions()
        self.companion_list.itemClicked.connect(self.show_details)

    def load_companions(self):
        # Load companion list from cloud config
        self.data = {
            "Nova": {"desc": "Elegant and witty AI assistant."},
            "Eve": {"desc": "Emotionally intuitive and warm."},
            "Axel": {"desc": "Rational strategist with dry humor."}
        }
        self.companion_list.addItems(self.data.keys())

    def show_details(self, item):
        name = item.text()
        desc = self.data.get(name, {}).get("desc", "No info")
        self.details.setText(f"🧠 {name}: {desc}")

    def activate(self):
        name = self.companion_list.currentItem().text()
        self.runtime.settings.set("active_companion", name)
        QMessageBox.information(self, "Activated", f"🤖 '{name}' is now your AI companion.")
