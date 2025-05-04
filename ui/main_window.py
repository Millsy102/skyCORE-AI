
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from ui.main_window_patch import CommandInputWidget
from ui.plugin_preview_tab import PluginPreviewTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("skyCORE-AI")
        self.resize(1000, 700)

        central = QWidget()
        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(CommandInputWidget(), "🧠 Chat / Commands")
        tabs.addTab(PluginPreviewTab(), "🧩 Plugin Preview")

        layout.addWidget(tabs)
        central.setLayout(layout)
        self.setCentralWidget(central)
