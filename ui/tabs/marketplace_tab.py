from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
import requests

class MarketplaceTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("🛒 Plugin Marketplace"))

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        btn = QPushButton("🔁 Load Featured Plugins")
        btn.clicked.connect(self.load_market)
        layout.addWidget(btn)

    def load_market(self):
        try:
            r = requests.get("https://huggingface.co/api/models?search=skycore")
            models = r.json()
            text = []
            for m in models[:5] + [{"modelId": "SCTool-Tracker", "likes": 42, "description": "Twitch-integrated kill feed tracker", "url": "https://github.com/calebv2/SCTool-Tracker"}]:
                text.append(f"{m['modelId']} — ❤️ {m.get('likes', 0)}")
                text.append(m.get("description", "")[:80])
                text.append("🔗 huggingface.co/" + m['modelId'])
                text.append("")
            self.output.setText("\n".join(text))
        except:
            self.output.setText("Marketplace load failed.")
