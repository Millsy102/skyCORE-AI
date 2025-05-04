# 📦 Module imports
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl
from src.logger import log

# Class: BrowserTab — defines main behavior for browser_engine.py
class BrowserTab(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://huggingface.co"))
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

# Function: load_url — handles a core step in this module
    def load_url(self, url):
        try:
            self.browser.setUrl(QUrl(url))
            log(f"[Browser] Loaded URL: {url}")
        except Exception as e:
            log(f"[Browser] Failed to load: {e}")