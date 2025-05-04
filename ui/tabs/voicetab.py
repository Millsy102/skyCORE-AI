
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox, QComboBox

class VoiceTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.enable_tts = QCheckBox("🔊 Enable TTS")
        self.enable_tts.setChecked(runtime.settings.get("tts_enabled", False))

        self.voice_selector = QComboBox()
        self.voice_selector.addItems(["Default", "Nova", "Echo", "Luna"])
        self.voice_selector.setCurrentText(runtime.settings.get("voice_model", "Default"))

        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.clicked.connect(self.save)

        layout.addWidget(QLabel("🎙️ AI Voice Settings"))
        layout.addWidget(self.enable_tts)
        layout.addWidget(self.voice_selector)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

    def save(self):
        self.runtime.settings.set("tts_enabled", self.enable_tts.isChecked())
        self.runtime.settings.set("voice_model", self.voice_selector.currentText())
        QMessageBox.information(self, "Saved", "✅ Voice settings updated.")
