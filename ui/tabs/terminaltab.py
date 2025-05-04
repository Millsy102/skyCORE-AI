
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
import subprocess

class TerminalTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.cmd_input = QTextEdit()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.run_btn = QPushButton("▶️ Run Command")
        self.run_btn.clicked.connect(self.run_cmd)

        layout.addWidget(self.cmd_input)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def run_cmd(self):
        cmd = self.cmd_input.toPlainText().strip()
        if not cmd:
            self.output.setText("⚠️ No command provided.")
            return
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.output.setText(result.stdout or result.stderr)
        except Exception as e:
            self.output.setText(f"❌ Error: {e}")
