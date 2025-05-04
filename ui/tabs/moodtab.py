
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class MoodTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.energy_slider = QSlider(Qt.Horizontal)
        self.energy_slider.setRange(0, 100)
        self.energy_slider.setValue(runtime.settings.get("mood_energy", 50))

        self.tone_slider = QSlider(Qt.Horizontal)
        self.tone_slider.setRange(0, 100)
        self.tone_slider.setValue(runtime.settings.get("mood_tone", 50))

        self.save_btn = QPushButton("💾 Save Mood")
        self.save_btn.clicked.connect(self.save_mood)

        layout.addWidget(QLabel("⚡ Energy Level"))
        layout.addWidget(self.energy_slider)
        layout.addWidget(QLabel("🎨 Tone Intensity"))
        layout.addWidget(self.tone_slider)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

    def save_mood(self):
        self.runtime.settings.set("mood_energy", self.energy_slider.value())
        self.runtime.settings.set("mood_tone", self.tone_slider.value())
        QMessageBox.information(self, "Saved", "✅ Mood settings saved.")
