
# ui/main_window_patch.py
from PySide6.QtWidgets import QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from ui.command_dispatcher import process_gui_input
import os

class CommandInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.send = QPushButton("Send")
        self.send.clicked.connect(self.run_command)

        layout = QVBoxLayout()
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        layout.addWidget(self.send)
        self.setLayout(layout)

    def run_command(self):
        user_text = self.input.text()
        self.output.append(f"> {user_text}")
        response = process_gui_input(user_text, os.getcwd())
        self.output.append(str(response))
