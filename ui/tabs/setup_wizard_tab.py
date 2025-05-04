from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import os
import json
import webbrowser

class SetupWizardTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("🧠 skyCORE-AI Setup Wizard"))

        self.twitch_user = QLineEdit()
        self.twitch_user.setPlaceholderText("Enter Twitch Username")
        layout.addWidget(self.twitch_user)

        self.access_token = QLineEdit()
        self.access_token.setPlaceholderText("Twitch Access Token")
        layout.addWidget(self.access_token)

        self.webhook = QLineEdit()
        self.webhook.setPlaceholderText("Optional Cloud Sync Webhook")
        layout.addWidget(self.webhook)

        self.run_btn = QPushButton("🔧 Apply Configuration")
        self.run_btn.clicked.connect(self.apply_config)
        layout.addWidget(self.run_btn)

        self.launch_btn = QPushButton("🎮 Launch Overlay Test")
        self.launch_btn.clicked.connect(self.launch_overlay)
        layout.addWidget(self.launch_btn)

        layout.addWidget(QLabel("✅ This wizard only runs on first install unless reset."))

    def apply_config(self):
        twitch_data = {
            "username": self.twitch_user.text().strip(),
            "access_token": self.access_token.text().strip()
        }
        os.makedirs("config", exist_ok=True)
        with open("config/twitch.json", "w") as f:
            json.dump(twitch_data, f, indent=2)

        cloud_data = {
            "sync_enabled": True,
            "webhook": self.webhook.text().strip(),
            "preferred_agent": "SkyDev",
            "overlays_enabled": True
        }
        with open("config/skycore_cloud.json", "w") as f:
            json.dump(cloud_data, f, indent=2)

        QMessageBox.information(self, "Setup", "✅ Configuration applied successfully!")

    def launch_overlay(self):
        panel_path = os.path.abspath("overlays/panel.html")
        if os.path.exists(panel_path):
            webbrowser.open(f"file://{panel_path}")
        else:
            QMessageBox.warning(self, "Overlay", "❌ Overlay file not found.")
