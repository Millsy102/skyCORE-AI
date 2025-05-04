
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import platform
import datetime
import psutil

class AboutTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)

        self.version_label = QLabel("skyCORE-AI v1.0.0")
        self.date_label = QLabel(f"Build Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        self.sys_label = QLabel(f"System: {platform.system()} {platform.release()}")
        self.cpu_label = QLabel("")
        self.mem_label = QLabel("")

        layout.addWidget(self.version_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.sys_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.mem_label)
        layout.addWidget(QLabel("🧑‍💻 Created by the skyCORE-AI Dev Team"))
        self.setLayout(layout)
        self.update_stats()

    def update_stats(self):
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        self.cpu_label.setText(f"⚙️ CPU Usage: {cpu}%")
        self.mem_label.setText(f"💾 RAM Usage: {mem}%")
