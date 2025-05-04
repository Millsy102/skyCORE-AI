from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
import os

class TraceTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("📜 skyCORE-AI Trace Viewer"))

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Filter by keyword...")
        self.search_bar.textChanged.connect(self.apply_filter)
        layout.addWidget(self.search_bar)

        self.trace_display = QTextEdit()
        self.trace_display.setReadOnly(True)
        layout.addWidget(self.trace_display)

        btns = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_logs)
        btns.addWidget(self.refresh_btn)

        self.export_btn = QPushButton("📁 Export")
        self.export_btn.clicked.connect(self.export_log)
        btns.addWidget(self.export_btn)

        self.copy_btn = QPushButton("📋 Copy Last 50")
        self.copy_btn.clicked.connect(self.copy_recent)
        btns.addWidget(self.copy_btn)

        layout.addLayout(btns)
        self.load_logs()

    def load_logs(self):
        path = "logs/skycore.log"
        if os.path.exists(path):
            with open(path, "r") as f:
                self.raw_log = f.read()
                self.trace_display.setText(self.raw_log)
        else:
            self.raw_log = ""
            self.trace_display.setText("No log found.")

    def apply_filter(self):
        keyword = self.search_bar.text().lower()
        lines = self.raw_log.splitlines()
        filtered = [l for l in lines if keyword in l.lower()]
        self.trace_display.setText("\n".join(filtered))

    def export_log(self):
        if not self.raw_log:
            QMessageBox.information(self, "Export", "No logs to export.")
            return
        with open("trace_export.log", "w") as f:
            f.write(self.raw_log)
        QMessageBox.information(self, "Export", "Trace exported to trace_export.log")

    def copy_recent(self):
        from PySide6.QtGui import QGuiApplication
        lines = self.raw_log.splitlines()[-50:]
        QGuiApplication.clipboard().setText("\n".join(lines))
        QMessageBox.information(self, "Copied", "Last 50 trace lines copied to clipboard.")
