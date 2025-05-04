
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QTextEdit, QPushButton, QHBoxLayout
from src.trace_logger import TraceLogger
from src.trace_replay_handler import TraceReplayHandler

class TraceTab(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = TraceLogger()
        self.replay = TraceReplayHandler()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.trace_list = QListWidget()
        self.trace_list.itemClicked.connect(self.display_trace)

        self.details = QTextEdit()
        self.details.setReadOnly(True)

        button_row = QHBoxLayout()
        self.replay_button = QPushButton("Replay")
        self.replay_button.clicked.connect(self.replay_selected)
        button_row.addWidget(self.replay_button)

        layout.addWidget(self.trace_list)
        layout.addLayout(button_row)
        layout.addWidget(self.details)

        self.load_traces()

    def load_traces(self):
        self.entries = self.logger.get_log()
        for i, entry in enumerate(self.entries):
            self.trace_list.addItem(f"{i+1}. {entry['input']}")

    def display_trace(self, item):
        index = self.trace_list.currentRow()
        entry = self.entries[index]
        text = f"Prompt: {entry['input']}\n\nResponse: {entry['response']}\nTokens: {entry['tokens_used']}"
        self.details.setPlainText(text)

    def replay_selected(self):
        index = self.trace_list.currentRow()
        result = self.replay.replay(index)
        self.details.append(f"\n[Replayed]\n{result['text']}")
