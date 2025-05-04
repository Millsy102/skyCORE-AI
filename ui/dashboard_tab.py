
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton,
    QLineEdit, QListWidget, QSplitter, QTabWidget, QFrame, QComboBox
)
from PySide6.QtCore import Qt, Signal
from src.ai_controller import AIController
from src.trace_logger import TraceLogger
from src.model_stats import ModelStats
from src.plugin_reflector import PluginReflector
from src.command_parser import CommandParser
from src.persona_manager import PersonaManager
from src.memory_manager import MemoryManager


class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()

        self.ai = AIController()
        self.trace_logger = TraceLogger()
        self.model_stats = ModelStats()
        self.plugin_reflector = PluginReflector()
        self.command_parser = CommandParser()
        self.persona_manager = PersonaManager()
        self.memory_manager = MemoryManager()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header
        header = QHBoxLayout()
        self.model_label = QLabel("Model: gpt-4")
        self.persona_dropdown = QComboBox()
        self.persona_dropdown.addItems(self.persona_manager.list_personas())
        self.persona_dropdown.currentTextChanged.connect(self.change_persona)
        self.token_label = QLabel("Tokens: 0")
        header.addWidget(self.model_label)
        header.addWidget(self.persona_dropdown)
        header.addStretch()
        header.addWidget(self.token_label)

        layout.addLayout(header)

        # Splitter: Left (prompt/response), Right (trace/context)
        splitter = QSplitter(Qt.Horizontal)

        # Left: Prompt/Response
        left_frame = QFrame()
        left_layout = QVBoxLayout()
        left_frame.setLayout(left_layout)

        self.prompt_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.on_send)

        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)

        input_row = QHBoxLayout()
        input_row.addWidget(self.prompt_input)
        input_row.addWidget(self.send_button)

        left_layout.addLayout(input_row)
        left_layout.addWidget(self.response_output)
# Plugin Output Dock
        self.plugin_output = QTextEdit()
        self.plugin_output.setReadOnly(True)
        left_layout.addWidget(QLabel("Plugin Output:"))
        left_layout.addWidget(self.plugin_output)

        # Right: Trace & Prompt Stack Viewer
        right_frame = QTabWidget()
        self.trace_list = QListWidget()
        self.stack_viewer = QTextEdit()
        self.stack_viewer.setReadOnly(True)
        right_frame.addTab(self.trace_list, "Trace")
        right_frame.addTab(self.stack_viewer, "Prompt Stack")

        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)
        splitter.setSizes([800, 300])

        layout.addWidget(splitter)

    def on_send(self):
        user_input = self.prompt_input.text()
        if not user_input:
            return

        # Handle commands first
        if user_input.startswith("/"):
            self.response_output.append("[CMD] Executing command...")
            cmd_result = self.command_parser.parse(user_input)
            self.response_output.append(cmd_result)
            return

        response = self.ai.respond(user_input)
        self.response_output.append(f"You: {user_input}")
        self.response_output.append(f"AI: {response['text']}")

        self.trace_logger.log(user_input, response)
        self.token_label.setText(f"Tokens: {response['tokens_used']}")

        full_stack = self.ai.build_prompt_stack(user_input)
        self.stack_viewer.setPlainText(full_stack)
        if response.get('plugins_triggered'):
            self.plugin_output.append(f"\n[Plugin Output]\n{response['text']}\n")
        self.trace_list.addItem(user_input)

        self.prompt_input.clear()


def change_persona(self, name):
        self.persona_manager.set_active(name)
        self.response_output.append(f"[Persona switched to: {name}]")
