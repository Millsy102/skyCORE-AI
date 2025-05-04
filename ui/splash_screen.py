from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap, Qt

class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(600, 300)
        pixmap.fill(Qt.white)
        super().__init__(pixmap)
        self.setWindowTitle("skyCORE-AI is Booting")
        self.showMessage("🔧 Initializing systems...", Qt.AlignBottom | Qt.AlignCenter, Qt.black)