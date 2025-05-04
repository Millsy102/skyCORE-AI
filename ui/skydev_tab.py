
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QTextEdit, QListWidget,
    QPushButton, QFileSystemModel, QTreeView, QTabWidget, QPlainTextEdit
)
from PySide6.QtCore import Qt, QDir
from src.skydev_runner import PluginTestRunner
from src.plugin_validator import PluginValidator
from src.skydev_ai_panel import SkyDevAIAssistant
from src.ui_reflector import UIReflector
from src.plugin_config_parser import PluginConfigParser


class SkyDevTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.runner = PluginTestRunner()
        self.validator = PluginValidator()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        splitter = QSplitter(Qt.Horizontal)

        # Left panel: File tree + AI assistant
        left_panel = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_panel)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.currentPath())
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(QDir.currentPath()))
        self.tree_view.clicked.connect(self.on_file_click)

        self.ai_panel = SkyDevAIAssistant()

        left_panel.addWidget(self.tree_view)
        left_panel.addWidget(self.ai_panel)

        # Right panel: Code editor tabs + tools
        right_tabs = QTabWidget()
        self.code_editors = {}

        # Tools tab
        tools_widget = QWidget()
        tools_layout = QVBoxLayout()
        tools_widget.setLayout(tools_layout)

        self.test_output = QTextEdit()
        self.test_output.setReadOnly(True)
        self.test_button = QPushButton("Run Plugin Tests")
        self.test_button.clicked.connect(self.run_tests)

        self.validation_output = QTextEdit()
        self.validation_output.setReadOnly(True)
        self.validate_button = QPushButton("Validate Plugin")
        self.validate_button.clicked.connect(self.run_validation)

        tools_layout.addWidget(self.test_button)
        tools_layout.addWidget(self.test_output)
        tools_layout.addWidget(self.validate_button)
        tools_layout.addWidget(self.validation_output)
self.meta_output = QTextEdit()
        self.meta_output.setReadOnly(True)
        self.meta_button = QPushButton("Show Plugin Metadata")
        self.meta_button.clicked.connect(self.show_plugin_metadata)
        tools_layout.addWidget(self.meta_button)
        tools_layout.addWidget(self.meta_output)

        right_tabs.addTab(tools_widget, "DevTools")

        splitter.addWidget(left_widget)
        splitter.addWidget(right_tabs)
        splitter.setSizes([300, 900])

        layout.addWidget(splitter)
        self.right_tabs = right_tabs

    def on_file_click(self, index):
        file_path = self.file_model.filePath(index)
        if file_path.endswith(('.py', '.yaml', '.json')):
if file_path.endswith('ui.yaml'):
                reflector = UIReflector()
                preview_widget = reflector.render_from_yaml(file_path)
                self.right_tabs.addTab(preview_widget, f"{file_path.split('/')[-1]} (Preview)")
            if file_path in self.code_editors:
                return
            editor = QPlainTextEdit()
            try:
                with open(file_path, 'r') as f:
                    editor.setPlainText(f.read())
            except Exception as e:
                editor.setPlainText(f"Failed to load file: {e}")

            self.right_tabs.addTab(editor, file_path.split('/')[-1])
            self.code_editors[file_path] = editor

    def run_tests(self):
        result = self.runner.run()
        self.test_output.setPlainText(result)

    def run_validation(self):
        result = self.validator.validate()
        self.validation_output.setPlainText(result)


def show_plugin_metadata(self):
        parser = PluginConfigParser()
        plugin_settings = parser.parse()
        meta = plugin_settings.get('__meta__', {})
        self.meta_output.setPlainText(f"Name: {meta.get('name', 'N/A')}\nAuthor: {meta.get('author', 'N/A')}\nVersion: {meta.get('version', 'N/A')}\nDescription: {meta.get('description', '')}")
