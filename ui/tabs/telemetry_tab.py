from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton
import os

class TelemetryTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)

        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter log by keyword")
        self.filter.textChanged.connect(self.apply_filter)
        layout.addWidget(self.filter)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        refresh = QPushButton("🔄 Refresh")
        refresh.clicked.connect(self.load_logs)
        layout.addWidget(refresh)

        self.raw = ""
        self.load_logs()

    def load_logs(self):
        if os.path.exists("logs/skycore.log"):
            with open("logs/skycore.log", "r") as f:
                self.raw = f.read()
                self.apply_filter()
        else:
            self.output.setText("No telemetry logs found.")

    def apply_filter(self):
        key = self.filter.text().lower()
        lines = self.raw.splitlines()
        filtered = [l for l in lines if key in l.lower()]
        self.output.setText("\n".join(filtered))
