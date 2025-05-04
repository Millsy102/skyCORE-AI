from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
import subprocess
import threading
import os
import time
import json

class KillTrackerControlTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("🧩 Kill Tracker Plugin Control"))

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.proc = None
        btn_row = QHBoxLayout()

        self.launch_btn = QPushButton("▶️ Launch Tracker UI")
        self.launch_btn.clicked.connect(self.launch_tracker)
        btn_row.addWidget(self.launch_btn)

        self.status_btn = QPushButton("📊 Show Kill Stats")
        self.status_btn.clicked.connect(self.show_kill_stats)
        btn_row.addWidget(self.status_btn)

        layout.addLayout(btn_row)

        twitch_row = QHBoxLayout()
        self.twitch_btn = QPushButton("🔄 Check Twitch Status")
        self.twitch_btn.clicked.connect(self.check_twitch_status)
        twitch_row.addWidget(self.twitch_btn)

        self.inject_btn = QPushButton("💉 Inject Dummy Kill")
        self.inject_btn.clicked.connect(self.inject_kill)
        twitch_row.addWidget(self.inject_btn)

        layout.addLayout(twitch_row)

    def launch_tracker(self):
        try:
            if self.proc is None or self.proc.poll() is not None:
                entry = os.path.join("plugins", "killTracker", "sctool_ui", "Kill_main.py")
                self.proc = subprocess.Popen(["python", entry], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                threading.Thread(target=self.read_output, daemon=True).start()
                self.output.append("🔄 Kill Tracker started...")
            else:
                self.output.append("⚠️ Kill Tracker already running.")
        except Exception as e:
            self.output.append(f"❌ {e}")

    def read_output(self):
        for line in self.proc.stdout:
            self.output.append(line.strip())

    def show_kill_stats(self):
        if hasattr(self.runtime, "memory"):
            kills = self.runtime.memory.get_all("kill_event")
            count = len(kills)
            victims = [k.get("victim", "?") for k in kills]
            self.output.append(f"🧠 {count} kills in memory.")
            for v in victims[-5:]:
                self.output.append(f" - {v}")
        else:
            self.output.append("⚠️ Memory unavailable.")

    def check_twitch_status(self):
        config_path = os.path.join("config", "twitch.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                data = json.load(f)
                self.output.append(f"📺 Twitch Config: {data.get('username')} @ {data.get('channel')}")
        else:
            self.output.append("⚠️ No Twitch config found.")

    def inject_kill(self):
        if hasattr(self.runtime, "memory"):
            dummy = {
                "victim": "PluginTestEnemy",
                "weapon": "debug_ray",
                "timestamp": time.time()
            }
            self.runtime.memory.add("kill_event", dummy)
            self.output.append("💉 Dummy kill event injected.")
        else:
            self.output.append("⚠️ Cannot inject — memory not found.")
