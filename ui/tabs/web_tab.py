
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView

class WebTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.url_bar = QLineEdit()
        self.view = QWebEngineView()
        self.go_btn = QPushButton("🌐 Go")
        self.go_btn.clicked.connect(self.load_page)
        layout.addWidget(self.url_bar)
        layout.addWidget(self.go_btn)
        layout.addWidget(self.view)
        self.setLayout(layout)

    def load_page(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.view.load(url)
