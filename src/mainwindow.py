
from PySide6.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout
from router import Router

class MainWindow(QMainWindow):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.setWindowTitle("skyCORE-AI")
        self.resize(1440, 900)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.router = Router(runtime, self.tabs)
        self.router.load_tabs()

        self.show()
