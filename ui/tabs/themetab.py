
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox
import os

class ThemeTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.themes = ["Dark", "Light", "Matrix", "Classic"]
        self.combo = QComboBox()
        self.combo.addItems(self.themes)
        self.combo.setCurrentText(runtime.settings.get("theme", "Dark"))

        self.apply_btn = QPushButton("🎨 Apply Theme")
        self.reset_btn = QPushButton("🔄 Reset to Default")

        self.apply_btn.clicked.connect(self.apply_theme)
        self.reset_btn.clicked.connect(self.reset_theme)

        layout.addWidget(QLabel("🎨 skyCORE-AI Theme Engine"))
        layout.addWidget(self.combo)
        layout.addWidget(self.apply_btn)
        layout.addWidget(self.reset_btn)
        self.setLayout(layout)

    def apply_theme(self):
        theme = self.combo.currentText()
        self.runtime.settings.set("theme", theme)
        QMessageBox.information(self, "Applied", f"✅ Theme '{theme}' saved. Restart for effect.")

    def reset_theme(self):
        self.combo.setCurrentText("Dark")
        self.runtime.settings.set("theme", "Dark")
        QMessageBox.information(self, "Reset", "🔄 Theme reset to 'Dark'")
