
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox
import os
import requests

class ExtensionHubTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.plugin_list = QListWidget()
        self.refresh_btn = QPushButton("🔄 Refresh Marketplace")
        self.install_btn = QPushButton("📥 Install Selected")
        self.uninstall_btn = QPushButton("🗑️ Uninstall Selected")

        self.refresh_btn.clicked.connect(self.refresh_plugins)
        self.install_btn.clicked.connect(self.install_plugin)
        self.uninstall_btn.clicked.connect(self.uninstall_plugin)

        layout.addWidget(QLabel("🧩 skyCORE-AI Extension Hub"))
        layout.addWidget(self.plugin_list)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.install_btn)
        layout.addWidget(self.uninstall_btn)
        self.setLayout(layout)

        self.refresh_plugins()

    def refresh_plugins(self):
        self.plugin_list.clear()
        try:
            # Simulated fetch from GitHub
            self.repo_plugins = ["notepad", "skydoc", "cloudsync"]
            self.plugin_list.addItems(self.repo_plugins)
        except:
            QMessageBox.warning(self, "Error", "⚠️ Failed to fetch plugin list.")

    def install_plugin(self):
        item = self.plugin_list.currentItem()
        if not item:
            return
        name = item.text()
        # Simulate install
        plugin_path = os.path.join("plugins", name)
        os.makedirs(plugin_path, exist_ok=True)
        with open(os.path.join(plugin_path, "main.py"), "w") as f:
            f.write("def register(self, *args, **kwargs):\n    print('Extension registered')")
            f.write("def register(self, *args, **kwargs):\n    print('Extension registered')")
        QMessageBox.information(self, "Installed", f"✅ {name} plugin installed.")

    def uninstall_plugin(self):
        item = self.plugin_list.currentItem()
        if not item:
            return
        name = item.text()
        path = os.path.join("plugins", name)
        if os.path.exists(path):
            os.system(f"rm -rf {path}" if os.name != 'nt' else f"rmdir /s /q {path}")
            QMessageBox.information(self, "Removed", f"🗑️ Plugin {name} uninstalled.")
