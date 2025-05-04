
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
import cv2

class VisionTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.label = QLabel("📷 Camera Preview")
        self.refresh = QPushButton("🔁 Refresh")
        self.refresh.clicked.connect(self.update)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.refresh)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(2000)

    def update(self):
        frame = self.runtime.vision_agent.get_frame()
        if frame is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(img))
