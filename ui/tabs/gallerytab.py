
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class GalleryTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("GalleryTab loaded. Replace this with full widget layout."))
        self.setLayout(layout)
