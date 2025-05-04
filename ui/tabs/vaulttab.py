
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QListWidget
import os

class VaultTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.path = os.path.join("plugins", "nsfw")

        layout = QVBoxLayout(self)
        self.refresh_btn = QPushButton("🔁 Refresh Vault")
        self.open_btn = QPushButton("📂 Open Vault Folder")
        self.plugin_list = QListWidget()
        self.refresh_btn.clicked.connect(self.refresh_list)
        self.open_btn.clicked.connect(self.open_folder)

        layout.addWidget(QLabel("🔐 NSFW Plugin Vault"))
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.plugin_list)
        self.setLayout(layout)
        self.refresh_list()

    def refresh_list(self):
        self.plugin_list.clear()
        if not os.path.exists(self.path):
            self.plugin_list.addItem("No NSFW plugins found.")
            return
        for name in os.listdir(self.path):
            self.plugin_list.addItem(name)

    def open_folder(self):
        os.system(f"start {self.path}" if os.name == 'nt' else f"open {self.path}")
