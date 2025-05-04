from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import json
import os

class SettingsTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("⚙️ SkyCore Settings"))
        layout.addWidget(QLabel("☁️ Cloud Sync Settings"))

        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Webhook / Sync Endpoint")
        layout.addWidget(self.webhook_input)

        self.cloud_btn = QPushButton("☁️ Push Config to Cloud")
        self.cloud_btn.clicked.connect(self.push_to_cloud)
        layout.addWidget(self.cloud_btn)

        self.reset_btn = QPushButton("🔁 Reset Setup Wizard")
        self.reset_btn.clicked.connect(self.reset_wizard)
        layout.addWidget(self.reset_btn)
        credits_btn = QPushButton("📄 View Credits")
        credits_btn.clicked.connect(self.show_credits)
        layout.addWidget(credits_btn)
    
    

        self.oauth_input = QLineEdit()
        self.oauth_input.setPlaceholderText("Twitch OAuth Token")
        layout.addWidget(self.oauth_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Twitch Bot Username")
        layout.addWidget(self.user_input)

        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText("Twitch Channel")
        layout.addWidget(self.channel_input)

        self.save_btn = QPushButton("💾 Save Twitch Settings")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        self.monitor_toggle = QPushButton("🎯 Toggle Kill Monitor")
        self.monitor_toggle.clicked.connect(self.toggle_monitor)
        layout.addWidget(self.monitor_toggle)

        self.config_file = "config/twitch.json"
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.oauth_input.setText(data.get("oauth", ""))
                self.user_input.setText(data.get("username", ""))
                self.channel_input.setText(data.get("channel", ""))

    def save_settings(self):
        data = {
            "oauth": self.oauth_input.text().strip(),
            "username": self.user_input.text().strip(),
            "channel": self.channel_input.text().strip()
        }
        os.makedirs("config", exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(data, f)
        QMessageBox.information(self, "Settings", "✅ Twitch settings saved.")

    def toggle_monitor(self):
        try:
            from plugins.killMonitor.plugin import Plugin
            plugin = Plugin()
            plugin.execute({"input": "start monitor"})
            QMessageBox.information(self, "Monitor", "🎯 Kill Monitor started.")
        except Exception as e:
            QMessageBox.warning(self, "Monitor", f"❌ {e}")


    def push_to_cloud(self):
        import json, requests
        try:
            config_path = "config/twitch.json"
            if os.path.exists(config_path):
                with open(config_path) as f:
                    data = json.load(f)
                endpoint = self.webhook_input.text().strip()
                if endpoint:
                    r = requests.post(endpoint, json=data)
                    QMessageBox.information(self, "Cloud Sync", f"☁️ Sync complete: {r.status_code}")
                else:
                    QMessageBox.warning(self, "Cloud Sync", "❌ No endpoint specified.")
        except Exception as e:
            QMessageBox.critical(self, "Cloud Sync", f"❌ Failed: {e}")
    

    def reset_wizard(self):
        try:
            lock_file = "config/.wizard_lock"
            if os.path.exists(lock_file):
                os.remove(lock_file)
            QMessageBox.information(self, "Reset Wizard", "🔁 Wizard will reappear on next launch.")
        except Exception as e:
            QMessageBox.critical(self, "Reset Wizard", f"❌ Error: {e}")
    

    def show_credits(self):
        try:
            with open("config/credits.json", "r") as f:
                data = json.load(f)

            msg = "🧾 Credits:\n"
            for k, v in data.items():
                msg += f"\nPlugin: {v.get('plugin')}\nAuthor: {v.get('author')}\n"
                msg += f"Website: {v.get('website')}\nDiscord: {v.get('discord')}\n"
            QMessageBox.information(self, "Credits", msg)
        except Exception as e:
            QMessageBox.critical(self, "Credits", f"❌ Failed to load credits: {e}")
    