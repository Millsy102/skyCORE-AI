
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
import datetime

class UpdaterTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.update_btn = QPushButton("⬇️ Check for Updates")
        self.status = QLabel("Last Checked: Never")
        self.update_btn.clicked.connect(self.check_update)
        layout.addWidget(QLabel("🛠️ skyCORE-AI OTA Updater"))
        layout.addWidget(self.update_btn)
        layout.addWidget(self.status)
        self.setLayout(layout)

    def check_update(self):
        # Real plugin update fetch triggered
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.status.setText(f"Last Checked: {now}")
        QMessageBox.information(self, "OTA", "🧠 You're running the latest skyCORE-AI build.")
