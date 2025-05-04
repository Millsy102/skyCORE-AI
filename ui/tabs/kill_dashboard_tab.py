from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QHBoxLayout
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
import time
import os
from src.services.tracker_service import TrackerService

class KillDashboardTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.tracker = TrackerService()
        self.kills = 0
        self.deaths = 0
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("🎯 Kill Dashboard + Twitch Status + Audio"))

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.stats = QLabel("K:D - 0:0 | Twitch: [unknown] | Clips: 0")
        layout.addWidget(self.stats)

        btn_row = QHBoxLayout()
        refresh = QPushButton("🔁 Refresh")
        refresh.clicked.connect(self.update_log)
        btn_row.addWidget(refresh)

        clip_btn = QPushButton("🎬 Create Clip")
        clip_btn.clicked.connect(self.make_clip)
        btn_row.addWidget(clip_btn)

        layout.addLayout(btn_row)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Send message to Twitch chat...")
        layout.addWidget(self.chat_input)

        send_btn = QPushButton("📤 Send to Chat")
        send_btn.clicked.connect(self.send_chat)
        layout.addWidget(send_btn)

        delay_row = QHBoxLayout()
        self.delay_input = QLineEdit()
        self.delay_input.setPlaceholderText("Set clip delay (s)")
        delay_row.addWidget(self.delay_input)
        delay_btn = QPushButton("🕒 Set Delay")
        delay_btn.clicked.connect(self.set_delay)
        delay_row.addWidget(delay_btn)
        layout.addLayout(delay_row)

        # Audio
        self.sound = QSoundEffect()
        wav_path = os.path.join("external/SCTool-Tracker-Git/kill.wav")
        if os.path.exists(wav_path):
            self.sound.setSource(QUrl.fromLocalFile(wav_path))

        self.chat_log = QTextEdit()
layout.addWidget(QLabel("🧠 Live Twitch Chat"))
self.chat_log.setReadOnly(True)
layout.addWidget(self.chat_log)
try:
    from src.services.twitch_chat_reader import TwitchChatReader
    self.reader = TwitchChatReader("oauth:your_oauth", "your_botname", "yourchannel")
    self.reader.message_received.connect(self.chat_log.append)
    self.reader.start()
except Exception as e:
    self.chat_log.setText(f"Twitch chat reader error: {e}")
self.update_log()
        def update_log(self):
    if self.runtime and hasattr(self.runtime, "memory"):
    kills = self.runtime.memory.get_all("kill_event")
    self.kills = len(kills)
            formatted = []
            for k in kills[-10:]:
                victim = k.get("victim", "???")
                weapon = k.get("weapon", "???")
                t = time.strftime('%H:%M:%S', time.localtime(k.get("timestamp", 0)))
                formatted.append(f"[{t}] {victim} defeated by {weapon}")
            self.log.setText("\n".join(formatted))
            if kills and self.sound.isLoaded():
                self.sound.play()

        auth_status = "✅" if self.tracker.state.get("authenticated") else "❌"
        self.stats.setText(f"K:D - {self.kills}:{self.deaths} | Twitch: {auth_status} | Clips: {len(self.tracker.state.get('kills', []))}")

    def make_clip(self):
        result = self.tracker.create_clip()
        self.log.append(f"🎬 {result}")
        self.chat_log = QTextEdit()
layout.addWidget(QLabel("🧠 Live Twitch Chat"))
self.chat_log.setReadOnly(True)
layout.addWidget(self.chat_log)
try:
    from src.services.twitch_chat_reader import TwitchChatReader
    self.reader = TwitchChatReader("oauth:your_oauth", "your_botname", "yourchannel")
    self.reader.message_received.connect(self.chat_log.append)
    self.reader.start()
except Exception as e:
    self.chat_log.setText(f"Twitch chat reader error: {e}")
self.update_log()

    def send_chat(self):
        msg = self.chat_input.text().strip()
        if msg:
            self.log.append(f"📤 Sending: {msg}")
            self.tracker.post_kill_message(msg)
            self.chat_input.clear()

    def set_delay(self):
        try:
            seconds = int(self.delay_input.text())
            self.tracker.state["clip_delay"] = seconds
            self.log.append(f"🕒 Clip delay set to {seconds}s")
        except:
            self.log.append("⚠️ Invalid delay")
